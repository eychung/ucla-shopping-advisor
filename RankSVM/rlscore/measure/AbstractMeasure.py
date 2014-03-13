
class Measure(object):
    """The abstract base class from which all performance measure
    implementations should be derived"""

    def setParameters(self, parameters):
        """Sets the parameter values of the performance measure.
        
        @param parameters: parameters for the kernel
        @type parameters: dictionary of key:value pairs"""
        #most performance measures do not need this
        pass

    def multiOutputPerformance(self, Y, Y_predicted, verbose=False):
        """Calculates performance for multiple outputs, returns the result as one number.
        Useful for model selection.
        
        @param Y: matrix of correct labels
        @type Y: numpy matrix
        @param Y_predicted: matrix of predicted labels
        @type Y_predicted: numpy matrix
        @return: performance
        @rtype: float
        """
        return 0.
    
        
    def wrapper(self, Y, Y_predicted, qids=None, verbose=False):
        """Calculates performance for multiple outputs, returns the result as list.
        Useful for obtaining human interpretable performance.
        
        @param Y: matrix of correct labels
        @type Y: numpy matrix
        @param Y_predicted: matrix of predicted labels
        @type Y_predicted: numpy matrix
        @param qids: list of lists of indices for averaging
        @type qids: list of lists of integers
        @return: performance
        @rtype: float
        """
        return [self.multiVariatePerformance(Y, Y_predicted, qids=qids, verbose=verbose)]
    
    
    def multiVariatePerformance(self, Y, Y_predicted, qids=None, verbose=False):
        if qids == None:
            return self.subsetPerformance(Y, Y_predicted, verbose=verbose)
        
        pred = 0
        nncount = 0
        for inds in qids:
            Y_sub = Y[inds]
            Y_predicted_sub = Y_predicted[inds]
            pred_sub = self.subsetPerformance(Y_sub, Y_predicted_sub, verbose=verbose)
            if not pred_sub == None:
                pred += pred_sub
                nncount += 1
        if nncount == 0:
            return None
        pred /= nncount
        return pred
    
    
    def subsetPerformance(self, Y, Y_predicted, verbose=False):
        return self.multiOutputPerformance(Y, Y_predicted, verbose=verbose)


    def comparePerformances(self, perf1, perf2):
        """Given two performance values returns 1 if the first implies better performance,
        zero if the performances are tied, and -1 if the second one is better
        Default behaviour assumes that the bigger the value, the better the performance.
        
        @param perf1: performance
        @type perf1: float
        @param perf2: performance
        @type perf2: float
        @return: 1, 0 or -1
        @rtype: integer"""
        if perf1 > perf2:
            return 1
        elif perf1 < perf2:
            return - 1
        else:
            return 0
    
    
    def isErrorMeasure(self):
        return False
    
    
    def getName(self):
        """Returns the name of the performance measure
        
        @return: name of the performance measure
        @rtype: string"""
        return "unimplemented performance measure"

    def checkOutputs(self, Y):
        """Checks that the outputs are of appropriate type for the measure
        
        @param Y: matrix correct labels, each column in a list corresponds to one task
        @type Y: numpy matrix
        """
        pass


class UndefinedPerformance(Exception):
    """Used to indicate that the performance is not defined for the
    given predictions and outputs."""
    #Examples of this type of issue are disagreement error, which
    #is undefined when all the true labels are the same, and
    #recall, which is not defined if there are no relevant
    #instances in the data set.

    def __init__(self, value):
        """Initialization
        
        @param value: the error message
        @type value: string"""
        self.value = value

    def __str__(self):
        return repr(self.value)
