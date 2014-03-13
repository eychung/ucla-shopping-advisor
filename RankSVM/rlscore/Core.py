import DataSources
import FileReader
import FileWriter
import sys
from measure import cDisagreement
from learner import RankBundle

DEFAULT_PARAMS = {DataSources.TIKHONOV_REGULARIZATION_PARAMETER:'1'}



class Core(object):
    """The high level interface to the RLScore. Allows initializing the
    learning process, training a model according to a chosen model selection
    strategy and writing it to a file"""

    def __init__(self, rpool):
        self.resource_pool = rpool
        if DataSources.TRAIN_FEATURES_VARIABLE in rpool:
            self.learner = RankBundle.RLS.createLearner(**rpool)
        else:
            self.learner = None
        self.measure =cDisagreement.Measure()
        self.verbose = True
    
    
    def run(self):
        #Train, if learner defined
        if self.learner != None:
            if self.verbose:
                print "Learning model"
            self.learnModel()
        #Make predictions, if model and test examples available
        if self.resource_pool.has_key(DataSources.MODEL_VARIABLE) and self.resource_pool.has_key(DataSources.PREDICTION_FEATURES_VARIABLE):
            if self.verbose:
                print "Making predictions on test data"
            self.predict()
        #Measure performance, if predictions, true labels and performance measure available
        if self.measure != None and self.resource_pool.has_key(DataSources.PREDICTED_LABELS_VARIABLE) and self.resource_pool.has_key(DataSources.TEST_LABELS_VARIABLE):
            self.evaluatePerformance()
    
    
    def getResourcePool(self):
        """Returns the resource pool object.
        @return: resource_pool: resource pool containing all the data necessary for the learning process
        @rtype: dict
        """
        return self.resource_pool
    
    
    def learnModel(self):
        """Learns the model using the chosen learner, and the chosen
        model selection strategy and performance measure if any.
        """
        
        if self.verbose:
            print "Training model with regularization parameter value %s" % self.resource_pool[DataSources.TIKHONOV_REGULARIZATION_PARAMETER]
        self.learner.train()
        self.resource_pool = self.learner.getResourcePool()
        model = self.learner.getModel()
        self.resource_pool[DataSources.MODEL_VARIABLE] = model
    
    
    def predict(self):
        model = self.resource_pool[DataSources.MODEL_VARIABLE]
        predictions = model.predictFromPool(self.resource_pool)
        self.resource_pool[DataSources.PREDICTED_LABELS_VARIABLE] = predictions
    
    
    def evaluatePerformance(self):
        correct = self.resource_pool[DataSources.TEST_LABELS_VARIABLE]
        predicted = self.resource_pool[DataSources.PREDICTED_LABELS_VARIABLE]
        q_partition = None
        if self.resource_pool.has_key(DataSources.PREDICTION_QIDS_VARIABLE):
            print "calculating performance as averages over queries"
            qs = self.resource_pool[DataSources.PREDICTION_QIDS_VARIABLE]
            q_partition = qs.folds
        self.measure.checkOutputs(correct)
        performance = self.measure.wrapper(correct, predicted, q_partition)
        measure_name = self.measure.getName()
        for i in range(len(performance)):
            if not performance[i] == None:
                print "Performance for task %d: %f %s" % (i + 1, performance[i], measure_name)
            else:
                print "Performance for task %d: undefined %s" % (i + 1, measure_name)
        self.resource_pool[DataSources.TEST_PERFORMANCE_VARIABLE] = performance



def loadCore(parameters, input_file, output_file, input_reader = {}, output_writer = {}):
    """Loads dynamically the modules necessary for learning
    @param modules: learner, kernel, mselection and measure
    @type modules: dictionary of type:module string pairs
    @param parameters: reggrid, regparam, kparam
    @type parameters: dictionary of parameter:value string pairs
    @param input_file: variable-file pairs for input data
    @type input_file: dictionary of variable:file string pairs
    @param output_file: variable-file pairs for output data
    @type output_file: dictionary of variable:file string pairs
    @param input_reader: file-reader pairs for input data
    @type input_reader: dictionary of file:reader string pairs
    @param output_writer: file-writer pairs for input data
    @type output_writer: dictionary of file:writer string pairs
    """
    
    rpool = {}
    for key in DEFAULT_PARAMS.keys():
        if not key in parameters:
            parameters[key] = DEFAULT_PARAMS[key]
    if 'importpath' in parameters:
        paths = parameters['importpath'].split(";")
        for path in paths:
            sys.path.append(path)
        del parameters['importpath']
    if "verbose" in parameters:
        verbose = (parameters["verbose"]=="True")
    else:
        verbose = True #Default
    
    file_readerobj = {}
    for varname in input_reader.keys():
        filename = input_file[varname]
        reader = input_reader[varname]
        module = reader.rsplit(".")[0]
        exec "import " + module
        reader = eval(reader+"(filename)")
        file_readerobj[filename] = reader
    variable_type_file = []
    for varname in input_file.keys():
        filename = input_file[varname]
        if DataSources.VARIABLE_TYPES.has_key(varname):
            vartype = DataSources.VARIABLE_TYPES[varname]
        else:
            vartype = None
        if not file_readerobj.has_key(filename):
            readerclass = FileReader.DEFAULT_READERS[vartype]
            readerobj = readerclass(filename)
            file_readerobj[filename] = readerobj
        variable_type_file.append((varname, vartype, filename))     
    if verbose == True:
        print "Reading input files"
    for varname, vartype, file in variable_type_file:
        reader = file_readerobj[file]
        reader.toRpool(rpool, varname, vartype)
    measure = cDisagreement.Measure()
    
    
    rpool[DataSources.PERFORMANCE_MEASURE_VARIABLE] = measure
    
    rpool.update(parameters)
    
    if not measure == None:
        measure.setParameters(rpool)
    core = Core(rpool)
    core.run()
    rpool = core.resource_pool
    
    writers = []
    for varname, filename in output_file.iteritems():
        vartype = DataSources.VARIABLE_TYPES[varname]
        if not output_writer.has_key(varname):
            writerclass = FileWriter.DEFAULT_WRITERS[vartype]
            writerobj = writerclass()
        else:
            writerclass = output_writer[varname]
            module = writerclass.rsplit(".")[0]
            exec "import " + module
            writerobj = eval(writerclass+"()")
        writerobj.fromRpool(rpool, varname, vartype)
        writers.append((writerobj, filename))
    
    for writerobj, filename in writers:
        writerobj.write(filename)
    
    return core

    

