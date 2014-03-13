#Utilities for reading in the files used by the
#RLS software package

from scipy import sparse
from scipy.io import mmread
from scipy.sparse import csc_matrix
import numpy
from numpy import float64
from numpy import mat
from numpy import matrix
from scipy.sparse.base import spmatrix

import DataSources
import cPickle 

def readFeatureFile(f):
    """Reads in the feature values and checks that the input file is correctly formatted.
    Returns the attribute values, comments, dimensionality of the feature space and number of
    nonzero attributes
    
    param f: open file
    @type f: file object
    @param subset: if supplied only the lines whose indices are in subset are read in (default None)
    @type subset: list of integers
    @return features, comments, dimensionality of feature space, number of nonzero features
    @rtype: list of integer-float pairs, list of strings, integer, integer"""

    #some interesting statistics are calculated
    f.seek(0)
    #Features and comments are returned to the caller 
    #The indexing, with respect to the instances, is the same in all the lists.
    #Each line in the source represents an instance
    #each row represents a feature, each column an instance
    rows = []
    columns = []
    values = []
    linecounter = 0
    feaspace_dim = 0
    for line in f:
        linecounter += 1
        #Empty lines and commented lines are passed over
        if len(line.strip()) == 0 or line[0] == '#':
            print "Warning: no inputs on line %d" % linecounter
            continue
        line = line.split("#",1)
        attributes = line[0].split()
        previous = -1
        #Attributes indices must be positive integers in an ascending order,
        #and the values must be real numbers.
        for att_val in attributes:
            if len(att_val.split(":")) != 2:
                raise Exception("Error when reading in feature file: feature:value pair %s on line %d is not well-formed\n" % (att_val, linecounter))
            index, value = att_val.split(":")
            try:
                index = int(index)
                value = float(value)
                if value != 0.:
                    rows.append(index)
                    columns.append(linecounter-1)
                    values.append(value)
            except ValueError:
                raise Exception("Error when reading in feature file: feature:value pair %s on line %d is not well-formed\n" % (att_val, linecounter))
            if not index > previous:
                raise Exception("Error when reading in feature file: line %d features must be in ascending order\n" % (linecounter))
            previous = index
            if index+1 > feaspace_dim:
                feaspace_dim = index+1
    #That's all folks
    row_size = feaspace_dim
    col_size = linecounter
    return rows, columns, values, row_size, col_size   



def readSparseMatrix(f):
    """Reads a sparse matrix representation of the data from an
    open file-like object that is provided
    
    @param source: lines of the attribute file (possibly an open file)
    @type source: iterable object
    @param subset: if supplied only the lines whose indices are in subset are read in (default None)
    @type subset: list of integers
    @param dimensionality: dimensionality of the feature space
    @type dimensionality: integer
    @return X, comments
    @rtype scipy sparse matrix, list of strings"""
    rows, columns, values, row_size, col_size   = readFeatureFile(f)
    X = sparse.coo_matrix((values,(rows,columns)),(row_size, col_size), dtype=float64)
    X = X.tocsc()
    return X


class AbstractReaderOld(object):
        
    def toRpool(self, rpool, varname, vartype = None):
        """Puts data to the given resource pool
        @param rpool: resource pool
        @type rpool: ResourcePool
        @param varname: name of the loaded variable
        @type varname: string
        @param vartype: class of the loaded variable
        @type vartype: class
        """
        if vartype == None:
            if DataSources.VARIABLE_TYPES.has_key(varname):
                vartype = DataSources.VARIABLE_TYPES[varname]
            else:
                vartype = DataSources.DataSource
        ds = vartype(self.data)
        rpool[varname] = ds


class AbstractReaderSimplified(object):
        
    def toRpool(self, rpool, varname, vartype = None):
        """Puts data to the given resource pool
        @param rpool: resource pool
        @type rpool: ResourcePool
        @param varname: name of the loaded variable
        @type varname: string
        @param vartype: class of the loaded variable
        @type vartype: class
        """
        rpool[varname] = self.data


class FeatureFile(AbstractReaderSimplified):
    
    def __init__(self, filename):
        """Reads in a RLScore format feature file 
        
        @param filename: path tofeature file
        @type filename: string"""
        f = open(filename)
        self.data = readSparseMatrix(f)
        f.close()



class DenseTextFile(AbstractReaderSimplified):
    
    def __init__(self, filename):
        """Reads in a text file in dense matrix format. Uses Numpy loadtxt.
        
        @param filename: path to text file in dense matrix format
        @type filename: string"""
        f = open(filename)
        #lines = f.readlines()
        values = []
        for line in f:
            values.append([float(x) for x in line.split()])
        self.data = numpy.mat(values)
        #self.data = numpy.loadtxt(f)
        #self.data = numpy.mat(self.data)
        #if self.data.shape[0] == 1:
        #    self.data = self.data.T
        f.close()


class NumpyFile(AbstractReaderSimplified):
    
    def __init__(self, filename):
        """Reads in a text file in dense matrix format. Uses Numpy load.
        
        @param filename: path to file in npy format
        @type filename: string"""
        f = open(filename)
        self.data = numpy.load(f)
        self.data = numpy.mat(self.data)
        f.close()


class MtxFile(AbstractReaderSimplified):
    
    def __init__(self, filename):
        """Reads in a text file in sparse MTX matrix format. Uses scipy.io mmread.
        
        @param filename: path to text file in sparse matrix format
        @type filename: string"""
        #f = open(filename)
        self.data = mmread(filename)
        #numpy.loadtxt(f)
        self.data = csc_matrix(self.data) #numpy.mat(self.data)
        #f.close()


class QidFile(AbstractReaderOld):
    
    def __init__(self, filename):
        """Reads in a Qid file 
        
        @param filename: path to qid file
        @type filename: string"""
        f = open(filename)
        self.readQids(f)
        self.mapQids()
        self.data = self.qids
        f.close()
    
    def readQids(self, f):
        """Reads the query id file, used typically with label ranking
        
        @param f: lines of the qid file (possibly an open file)
        @type f: iterable object"""
        qids = []
        for line in f:
            qid = line.strip()
            qids.append(qid)
        #Check that at least some queries contain more than one example
        if len(qids) == len(set(qids)):
            raise Exception("Error in the qid file: all the supplied queries consist only of a single example\n")
        self.qids = qids
        
    def mapQids(self):
        """Maps qids to running numbering starting from zero, and partitions
        the training data indices so that each partition corresponds to one
        query"""
        #Used in FileReader, rls_predict
        qid_dict = {}
        folds = {}
        qid_list = []
        counter = 0
        for index, qid in enumerate(self.qids):
            if not qid in qid_dict:
                qid_dict[qid] = counter
                folds[qid] = []
                counter += 1
            qid_list.append(qid_dict[qid])
            folds[qid].append(index)
        final_folds = []
        for f in folds.values():
            final_folds.append(f)
        self.qids = qid_list
        self.folds = final_folds


class PickleReader(AbstractReaderSimplified):
    
    def __init__(self, filename):
        """ Loads data from a pickled file.
        @param filename: path to file containing pickled data
        @type filename: string
        """
        f = open(filename, 'rb')
        self.data = cPickle.load(f)
        f.close()


class SVMlightFile(AbstractReaderSimplified):
    
    def toRpool(self, rpool, varname, vartype = None):
        if vartype == None:
            vartype = DataSources.VARIABLE_TYPES[varname]
        composite = vartype()
        featurevarname = composite.getFVN()
        rpool[featurevarname] = self.fs
        labelvarname = composite.getLVN()
        rpool[labelvarname] = self.ls
        if not self.qs == None:
            qidvarname = composite.getQVN()
            rpool[qidvarname] = self.qs
    
    
    def __init__(self, filename):
        """ Loads examples from an SVM-light format data file. The
        file contains attributes, one label per example and optionally
        qids.
        @param filename: path to SVM-light file
        @type filename: string
        """
        f = open(filename)
        #some interesting statistics are calculated
        labelcount = None
        linecounter = 0
        feaspace_dim = 0
        #Features, labels, comments and possibly qids are later returned to caller
        #The indexing, with respect to the instances, is the same in all the lists.
        qids = None
         
        rows = []
        columns = []
        values = []
        
        all_outputs = []
        
        #Each line in the source represents an instance
        for linenumber, line in enumerate(f):
            if line[0] == "#" or line.strip() == "":
                continue
            linecounter += 1
            line = line.split('#')
            line = line[0].split()
            labels = line.pop(0)
            if line[0].startswith("qid:"):
                qid = line.pop(0)[4:]
                if qids == None:
                    if linecounter > 1:
                        raise Exception("Error when reading in SVMLight file: Line %d has a qid, previous lines did not have qids defined" % (linenumber))   
                    else:
                        qids = [qid]
                else:
                    qids.append(qid)
            else:
                if qids != None:
                    raise Exception("Error when reading in SVMLight file: Line %d has no qid, previous lines had qids defined" % (linenumber))
            attributes = line
            #Multiple labels are allowed, but each instance must have the
            #same amount of them. Labels must be real numbers.
            labels = labels.split("|")
            if labelcount == None:
                labelcount = len(labels)
            #Check that the number of labels is the same for all instances
            #and that the labels are real valued numbers.
            else:
                if labelcount != len(labels):
                    raise Exception("Error when reading in SVMLight file: Number of labels assigned to instances differs.\n First instance had %d labels whereas instance on line %d has %d labels\n" % (labelcount, linenumber, len(labels)))
            label_list = []
            #We check that the labels are real numbers and gather them
            for label in labels:
                try:
                    label = float(label)
                    label_list.append(label)
                except ValueError:
                    raise Exception("Error when reading in SVMLight file: label %s on line %d not a real number\n" % (label, linenumber))
            all_outputs.append(label_list)
            previous = 0
            #Attributes indices must be positive integers in an ascending order,
            #and the values must be real numbers.
            for att_val in attributes:
                if len(att_val.split(":")) != 2:
                    raise Exception("Error when reading in SVMLight file: feature:value pair %s on line %d is not well-formed\n" % (att_val, linenumber))
                index, value = att_val.split(":")
                try:
                    index = int(index)
                    value = float(value)
                    if value != 0.:
                        rows.append(index-1)
                        columns.append(linecounter-1)
                        values.append(value)
                except ValueError:
                    raise Exception("Error when reading in SVMLight file: feature:value pair %s on line %d is not well-formed\n" % (att_val, linecounter))
                if not index > previous:
                    raise Exception("Error when reading in SVMLight file: line %d features must be in ascending order\n" % (linecounter))
                previous = index
                if index > feaspace_dim:
                    feaspace_dim = index
        X = sparse.coo_matrix((values,(rows,columns)),(feaspace_dim, linecounter), dtype=float64)
        X = X.tocsc()
        self.fs = X
        Y = mat(all_outputs)
        self.ls = Y
        if not qids == None:
            self.qs = DataSources.QidSource(qids)
        else:
            self.qs = None
        f.close()


DEFAULT_READERS = {
                   spmatrix: FeatureFile,
                   matrix: DenseTextFile,
                   DataSources.QidSource: QidFile,
                   'model': PickleReader,
                   DataSources.TrainingSetCompositeVariable: SVMlightFile,
                   DataSources.TestSetCompositeVariable: SVMlightFile
                   }


