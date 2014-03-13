#Module for writing files
import cPickle

import numpy
from scipy import sparse

import DataSources




class AbstractWriter(object):
        
    def fromRpool(self, rpool, varname, vartype=None):
        """Takes data from the given resource pool into the writer object
        @param rpool: resource pool from which the data is taken
        @type rpool: dict
        @param varname: name of the variable to be saved
        @type varname: string
        @param vartype: class of the variable to be saved
        @type vartype: class
        """
        self.data = rpool[varname]
    
    def write(self, filename):
        """Saves data into a file.
        @param filename: name of the file into which the data is saved
        @type filename: string
        """


class PickleWriter(AbstractWriter):
    
    def write(self, filename):
        f = open(filename,'wb')
        cPickle.dump(self.data, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()


class DenseTextFile(AbstractWriter):
    
    def write(self, filename):
        numpy.savetxt(filename, self.data)
        #if isinstance(self.data, scipy.sparse.base.spmatrix):
        #    numpy.savetxt(filename, self.data.todense())
        #else:
        #    numpy.savetxt(filename, self.data)
        #f = open(filename, 'w')
        #data = self.data.T
        #rlen, clen = data.shape
        #for i in range(rlen):
        #    ss = ''
        #    for j in range(clen):
        #        ss += ' ' + str(data[i, j])
        #    f.write(ss + '\n')
        #    f.flush()
        #f.close()




class FeatureFile(AbstractWriter):
    
    def write(self, filename):
        f = open(filename, 'w')
        data = self.data.T
        rlen, clen = data.shape
        for i in range(rlen):
            ss = ''
            for j in range(clen):
                if data[i, j] != 0:
                    ss += ' ' + str(j) + ':' + str(data[i, j])
            ss = ss.strip()
            f.write(ss + '\n')
            f.flush()
        f.close()




class NumpyFile(AbstractWriter):
    
    def write(self, filename):
        data = self.data
        if isinstance(self.data, sparse.spmatrix):
            data = data.todense()
        numpy.save(filename, data)


class IndexListFile(AbstractWriter):
    
    def write(self, filename):
        numpy.savetxt(filename, self.data, fmt='%i')


class FloatListFile(AbstractWriter):
    
    def write(self, filename):
        numpy.savetxt(filename, self.data, fmt='%f')


DEFAULT_WRITERS = {
                   numpy.matrix: DenseTextFile,
                   'model': PickleWriter,
                   }

