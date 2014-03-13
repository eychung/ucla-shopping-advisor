
from scipy import sparse

import DataSources


class AbstractModel(object):
    
    def predictFromPool(self, rpool):
        """Makes real-valued predictions for new examples
        @param rpool: resource pool from which test data is read from
        @type rpool: dict
        @return: predictions, one column per task
        @rtype: numpy matrix of floats"""
        pass


class LinearModelWithBias(AbstractModel):
    """Represents a linear model for making predictions. New predictions are made
    by multiplying the feature vectors of new examples with the learned hyperplane
    plus a constant bias."""
    
    def __init__(self, W, b):
        """Initializes a primal model
        @param W: coefficients of the linear model, one column per task
        @type W: numpy matrix
        @param b: bias of the model, one column per task
        @type b: numpy matrix
        """
        self.W = W
        self.b = b
    
    
    def predictFromPool(self, rpool):
        """Makes real-valued predictions for new examples
        @param rpool: resource pool from which test data is read from
        @type rpool: dict
        @return: predictions, one column per task
        @rtype: numpy matrix of floats"""
        X = rpool[DataSources.PREDICTION_FEATURES_VARIABLE]
        return self.predict(X)
    
    
    def predict(self, X):
        W = self.W
        if X.shape[0] > W.shape[0]:
            #print 'Warning: the number of features ('+str(X.shape[0])+') in the data point for which the prediction is to be made is larger than the size ('+str(self.W.shape[0])+') of the predictor. Slicing the feature vector accordingly.'
            X = X[range(W.shape[0])]
        if X.shape[0] < W.shape[0]:
            #print 'Warning: the number of features ('+str(X.shape[0])+') in the data point for which the prediction is to be made is smaller than the size ('+str(self.W.shape[0])+') of the predictor. Slicing the predictor accordingly.'
            W = W[range(X.shape[0])]
        pred = X.T * W
        if isinstance(pred, sparse.spmatrix):
            pred = pred.todense()
        return pred + self.b

