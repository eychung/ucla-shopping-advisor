import AbstractMeasure
from AbstractMeasure import UndefinedPerformance

class Measure(AbstractMeasure.Measure):
    """The abstract base class from which all performance measures which are
    defined in terms of a single output should be inherited from (this includes
    most of the popular performance measures excluding multiclass ones). Multioutput
    performance is in this case calculated by invoking the single output measure
    seperately for each output."""


    def getPerformance(self, correct, predictions):
        """"Returns the performance given correct and predicted values.
        
        @param correct: correct output values
        @type correct: numpy matrix of floats
        @param predictions: predicted output values
        @type predictions: numpy matrix of floats"""
        
        #        This method must be implemented by the inheriting class
        raise Exception("routine getPerformance not implemented by the used performance measure")


    def multiOutputPerformance(self, Y, Y_predicted, verbose=False):
        performances = self.multiTaskPerformance(Y, Y_predicted, verbose=verbose)
        performance = self.aggregate(performances)
        return performance
    
    
    def wrapper(self, Y, Y_predicted, qids=None, verbose=False):
        
        performances = []
        for i in range(Y.shape[1]):
            #Columns are converted to lists, before calling the performance evaluation
            #function
            try:
                
                perf = self.multiVariatePerformance(Y[:,i], Y_predicted[:,i], qids=qids, verbose=verbose)
                performances.append(perf)
            #If performance is undefined the performances list simply gets a None value,
            #if in verbose mode, the warning message given by the baseclass which raised
            #the exception is printed out. It is deemed acceptable that for some of the
            #tasks performance cannot be calculated.
            except UndefinedPerformance, e:
                if verbose:
                    print "Warning:", e
                performances.append(None)
        return performances
    
    
    def subsetPerformance(self, Y, Y_predicted, verbose=False):
        try:
            #perf = self.getPerformance(Y.T.tolist()[0], Y_predicted.T.tolist()[0])
            perf = self.getPerformance(Y, Y_predicted)
            return perf
        except UndefinedPerformance, e:
            if verbose:
                print "Warning:", e
            return None


    def multiTaskPerformance(self, Y, Y_predicted, verbose=False):  
        """Estimates the performance for several tasks in parallel.
        
        @param Y: correct labels, one column per task
        @type Y: numpy.matrix
        @param Y_predicted: predicted labels, one column per task
        @type Y_predicted: numpy.matrix
        @param verbose: verbosity (default False)
        @type verbose: boolean
        @return: performances
        @rtype: list of floats
        """
        performances = []
        for i in range(Y.shape[1]):
            #Columns are converted to lists, before calling the performance evaluation
            #function
            try:
                #perf = self.getPerformance(Y[:,i].T.tolist()[0], Y_predicted[:,i].T.tolist()[0])
                perf = self.getPerformance(Y[:,i], Y_predicted[:,i])
                performances.append(perf)
            #If performance is undefined the performances list simply gets a None value,
            #if in verbose mode, the warning message given by the baseclass which raised
            #the exception is printed out. It is deemed acceptable that for some of the
            #tasks performance cannot be calculated.
            except UndefinedPerformance, e:
                if verbose:
                    print "Warning:", e
                performances.append(None)
        return performances
    
    
    def aggregate(self, performances):
        perf = 0.
        counter = 0
        for performance in performances:
            if performance != None:
                perf += performance
                counter += 1
        if counter == 0:
            return None
        perf /= counter
        return perf
