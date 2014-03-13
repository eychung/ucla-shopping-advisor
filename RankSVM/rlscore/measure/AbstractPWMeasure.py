import AbstractSingleOutputMeasure
import sys

class Measure(AbstractSingleOutputMeasure.Measure):
    """Abstract base class for performance measures which support the leave-pair-out estimate.
    Typically these would be ranking based measures, such as AUC or disagreement error"""

    def pairwisePerformance(self, pairs, Y, index, predicted):
        """Used for LPO-cross-validation. Performance measures can differ on which pairs
        are required, this is reflected in the getPairs method
        
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
        sys.stderr.write("Error: routine pairwisePerformance not implemented by the used performance measure\n")
        sys.exit(0)


    def getPairs(self, Y, i):
        """Returns the pairs used in LPO cross-validation
        Default behaviour is to return simply all pairs
        
        @param Y: matrix of correct labels, each column corresponds to one task
        @type Y: numpy matrix
        @return: list of lists of index pairs
        @rtype list of lists of integer pairs"""
        pairs = []
        for i in range(Y.shape[0]-1):
            for j in range(i+1, Y.shape[0]):
                pairs.append((i,j))
        return pairs
