#Disagreement error, a standard ranking measure.
import AbstractPWMeasure
from AbstractMeasure import UndefinedPerformance

class Measure(AbstractPWMeasure.Measure):
    """Disagreement error performance measure"""


    def getPerformance(self, correct, predictions):
        assert len(correct) == len(predictions)
        disagreement = 0.
        decisions = 0.
        for i in range(len(correct)):
            for j in range(len(correct)):
                    if correct[i] > correct[j]:
                        decisions += 1.
                        if predictions[i] < predictions[j]:
                            disagreement += 1.
                        elif predictions[i] == predictions[j]:
                            disagreement += 0.5
        #Disagreement error is not defined for cases where there
        #are no disagreeing pairs
        if decisions == 0:
            raise UndefinedPerformance("No pairs, all the instances have the same output")
        else:
            disagreement /= decisions
        return disagreement
    
    def pairwisePerformance(self, pairs, Y, index, predicted):
        """Used for LPO-cross-validation. The pairs supplied should be those with differing correct
        labels.
        
        @param pairs: a list of tuples of length two, containing the indices of the pairs in Y
        @type pairs: list of integer pairs
        @param Y: matrix of correct labels, each column corresponds to one task
        @type Y: numpy matrix
        @param index: the index of the task considered, this corresponding to a given column of Y
        @type index: integer
        @param predicted: a list of tuples of length two, containing the predictions for the pairs
        @type predicted: list of float pairs
        @return: performance
        @rtype: float"""
        if len(predicted) == 0:
            return None
            #raise UndefinedPerformance, "No pairs, all the instances have the same output"
        disagreement = 0.
        for pair in predicted:
            if pair[0] < pair[1]:
                disagreement += 1.
            elif pair[0] == pair[1]:
                disagreement += 0.5
        disagreement /= len(predicted)
        return disagreement

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
        if perf1 < perf2:
            return 1
        elif perf1 > perf2:
            return - 1
        else:
            return 0

    def getPairs(self, Y, index):
        """Returns pairs with differing labels.
        
        @param Y: matrix of correct labels, each column corresponds to one task
        @type Y: numpy matrix
        @return: list of lists of index pairs
        @rtype list of lists of integer pairs"""
        pairs = []
        tsetsize = Y.shape[0]
        for i in range(tsetsize - 1):
            for j in range(i + 1, tsetsize):
                if Y[i, index] > Y[j, index]: 
                    pairs.append((i, j))
                elif Y[i, index] < Y[j, index]:
                    pairs.append((j, i))
        return pairs

    
    def getName(self):
        return "disagreement error"
