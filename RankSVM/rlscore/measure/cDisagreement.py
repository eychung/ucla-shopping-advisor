import disagreement
import DisagreementMeasure
from AbstractMeasure import UndefinedPerformance
import operator
from numpy import array

class Measure(DisagreementMeasure.Measure):
    
    def getPerformance(self, correct, predictions):
        assert len(correct) == len(predictions)
        C = array(correct).reshape(len(correct),)
        C.sort()
        pairs = 0
        c_ties = 0
        for i in range(1, len(C)):
            if C[i] != C[i-1]:
                c_ties = 0
            else:
                c_ties += 1
            #this example forms a pair with each previous example, that has a lower value
            pairs += i-c_ties
        if pairs == 0:
            raise UndefinedPerformance("No pairs, all the instances have the same output")
        P = [(x, y) for y, x in enumerate(predictions)]
        P.sort(key=operator.itemgetter(0))
        P = [x[1] for x in P]
        #c code will not work, unless we ensure this
        correct = array(correct).reshape(correct.shape[0],)
        predictions = array(predictions).reshape(predictions.shape[0],)
        swapped = disagreement.swapped_pairs(correct, predictions, P)
        perf = float(swapped)/float(pairs)
        return perf
