
from numpy import float64, zeros

import AbstractLearner
from .. import DataSources


class RLS(AbstractLearner.RLS):
    '''RLS learner module for performing regularized least-squares regression or classification.'''
    
    
    def loadResources(self):
        AbstractLearner.RLS.loadResources(self)
        Y = self.resource_pool[DataSources.TRAIN_LABELS_VARIABLE]
        self.setLabels(Y)
    
    
    def requiredResources(self):
        names = []
        names.append(DataSources.TRAIN_LABELS_VARIABLE)
        return names
    
    
    def setLabels(self, Y):
        """
        Sets the label data for RLS.
        
        @param Y: Labels of the training examples. Can be either a single-column matrix (single output) or a multi-column matrix (multiple output).
        @type Y: numpy.matrix
        """
        
        self.Y = Y
        
        #Number of training examples
        self.size = Y.shape[0]
        
        #Number of outputs per training example
        self.ysize = Y.shape[1]
    
    
    def supportsModelSelection(self):
        return True
    
    
    def computeHO(self, indices):
        """Method for computing hold-out predictions for a trained RLS.
        
        @param indices: A list of indices of training examples belonging to the set for which the hold-out predictions are calculated. The list can not be empty.
        @type indices: a list of integers
        @return: Hold-out predictions as a matrix, whose rows are indexed by the training examples and columns by labels.
        @rtype: numpy.matrix
        @raise Exception: when the indices list is empty or if the same index is in the index set more than once.
        """
        
        self.checkHoldOutSet(indices)
        return zeros((self.size, self.ysize), dtype=float64)
    
    
    def checkHoldOutSet(self, indices):
        """Checks the consistency of the hold-out hold-out set with the trained learner.
        
        @param indices: A list of indices of training examples belonging to the set for which the hold-out predictions are calculated.
        @type indices: a list of integers
        @raise Exception: when the indices list not consistent with the learner.
        """
        
        if len(indices) == 0:
            raise Exception('Hold-out predictions can not be computed for an empty hold-out set.')
        
        if len(indices) != len(set(indices)):
            raise Exception('Hold-out can have each index only once.')

