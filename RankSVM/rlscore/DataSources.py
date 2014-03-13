#Sources for wrapping around data objects
from numpy import matrix
from scipy.sparse.base import spmatrix

from measure import AbstractMeasure


class DataSource(object):
    
    def __init__(self, data):
        self.data = data
    
    def getData(self):
        return self.data


class QidSource(DataSource):
    
    def __init__(self, qids):
        
        self.qids = qids
        self.mapQids()
    
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
    
    def readQids(self):
        """Returns query ids
        
        @return list of identifiers
        @rtype list of strings"""
        
        return self.qids


class TrainingSetCompositeVariable(object):
    
    def getFVN(self):
        return TRAIN_FEATURES_VARIABLE
    
    def getLVN(self):
        return TRAIN_LABELS_VARIABLE
    
    def getQVN(self):
        return TRAIN_QIDS_VARIABLE


class TestSetCompositeVariable(object):
    
    def getFVN(self):
        return PREDICTION_FEATURES_VARIABLE
    
    def getLVN(self):
        return TEST_LABELS_VARIABLE
    
    def getQVN(self):
        return PREDICTION_QIDS_VARIABLE


TRAIN_FEATURES_VARIABLE = 'train_features'
TRAIN_LABELS_VARIABLE = 'train_labels'
TRAIN_QIDS_VARIABLE = 'train_qids'
MODEL_VARIABLE = 'model'
PREDICTION_FEATURES_VARIABLE = 'prediction_features'
PREDICTION_QIDS_VARIABLE = 'test_qids'
PREDICTED_LABELS_VARIABLE = 'predicted_labels'
TEST_LABELS_VARIABLE = 'test_labels'
TEST_PERFORMANCE_VARIABLE = 'test_performance'
TRAIN_SET_VARIABLE = 'train_set'
TEST_SET_VARIABLE = 'test_set'
PERFORMANCE_MEASURE_VARIABLE = 'measure_obj'

TIKHONOV_REGULARIZATION_PARAMETER = 'regparam'



VARIABLE_TYPES = {
                  TRAIN_FEATURES_VARIABLE: spmatrix,
                  PREDICTION_FEATURES_VARIABLE: spmatrix,
                  TRAIN_LABELS_VARIABLE: matrix,
                  TEST_LABELS_VARIABLE: matrix,
                  PREDICTED_LABELS_VARIABLE: matrix,
                  TRAIN_QIDS_VARIABLE: QidSource,
                  PREDICTION_QIDS_VARIABLE: QidSource,
                  MODEL_VARIABLE: 'model',
                  PERFORMANCE_MEASURE_VARIABLE: AbstractMeasure.Measure,
                  TRAIN_SET_VARIABLE: TrainingSetCompositeVariable,
                  TEST_SET_VARIABLE: TestSetCompositeVariable
                  }

