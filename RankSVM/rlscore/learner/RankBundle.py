#A simple bundle solver for regularized empirical risk
#minimization. Used for RankSVM training. Requires cvxopt

import AbstractSupervisedLearner
import L2Optimizer
from .. import DataSources
from numpy import zeros
from numpy import mat
from numpy.linalg import norm
import RankSVM
from .. import Model
from scipy import sparse

class RLS(AbstractSupervisedLearner.RLS):


    def loadResources(self):
        """
        Loads the resources from the previously set ResourcePool object.
        
        @raise Exception: when some of the resources required by the learner is not available in the ResourcePool object.
        """
        AbstractSupervisedLearner.RLS.loadResources(self)
        self.X = self.resource_pool[DataSources.TRAIN_FEATURES_VARIABLE]
        if DataSources.TRAIN_QIDS_VARIABLE in self.resource_pool:
            qsource = self.resource_pool[DataSources.TRAIN_QIDS_VARIABLE]
            qids = qsource.readQids()
            self.setQids(qids)
        else:
            self.indslist = None
        if self.resource_pool.has_key('max_iterations'):
            self.maxiter = int(self.resource_pool['max_iterations'])
        else:
            self.maxiter = 500
        if DataSources.TIKHONOV_REGULARIZATION_PARAMETER in self.resource_pool:
            self.regparam = float(self.resource_pool[DataSources.TIKHONOV_REGULARIZATION_PARAMETER])
            assert self.regparam > 0
        else:
            self.regparam = 1.0
        if 'epsilon' in self.resource_pool:
            self.e = float(self.resource_pool['epsilon'])
            assert self.e > 0
        else:
            self.e = 0.001

    def setQids(self, qids):
        """Sets the qid parameters of the training examples. The list must have as many qids as there are training examples.
        
        @param qids: A list of qid parameters.
        @type qids: List of integers."""
        
        if len(qids) != self.size:
            qc = str(len(qids))
            ss = str(self.size)
            raise Exception('The number ' + ss + ' of training feature vectors is different from the number ' + qc + " of training qids.")
        
        self.qidlist = qids
        
        self.qidmap = {}
        for i in range(len(qids)):
            qid = qids[i]
            if self.qidmap.has_key(qid):
                sameqids = self.qidmap[qid]
                sameqids.append(i)
            else:
                self.qidmap[qid] = [i]
        self.indslist = []
        for qid in self.qidmap.keys():
            self.indslist.append(self.qidmap[qid])
           

    def setLabels(self, Y):
        """
        Sets the label data for RLS.
        
        @param Y: Labels of the training examples. Should be a single column matrix.
        @type Y: numpy.matrix
        """
        
        self.Y = Y
        
        #Number of training examples
        self.size = Y.shape[0]
        
        if not Y.shape[1] == 1:
            raise Exception('L2BundleLearner supports only one output at a time. The output matrix is now of shape ' + str(Y.shape) + '.')

    def requiredResources(self):
        """
        Returns the names of the DataSources corresponding to the resources required by the learner.
        
        @return: a list of class names of the subclasses of the DataSource class.
        @rtype: list
        """
        
        names = []
        names.append(DataSources.TRAIN_FEATURES_VARIABLE)
        names.append(DataSources.TRAIN_LABELS_VARIABLE)
        return names
    
    def train(self, w0 = None):
        regparam = self.regparam
        if w0 == None:
            w = mat(zeros(self.X.shape[0])).T
        else:
            w = w0
        if type(self.X)== sparse.csc_matrix:
            self.loss = RankSVM.SparseRankSVMLoss(self.X, self.Y, self.indslist)
            print "Sparse data"
        else:
            self.loss = RankSVM.DenseRankSVMLoss(self.X, self.Y, self.indslist)
            print "Dense data"
        self.regularizer = L2Regularizer(regparam)
        self.optimizer = L2Optimizer.PrimalDualOptimizer(regparam, self.X.shape[0])
        t = 0
        e_t = self.e+1.0
        model = []
        ubound_loss = None
        lbound_loss = None
        W_best = None
        loss, a = self.loss.loss_gradient(w)
        while e_t> self.e and t< self.maxiter:
            t = t+1
            b = loss-(w.T*a)[0,0]
            self.optimizer.add_bundle(a, b)
            model.append((a,b))
            w = self.optimizer.optimize()
            loss, a = self.loss.loss_gradient(w)
            ub_loss = loss + self.regularizer.value(w)
            if (ubound_loss == None) or ub_loss < ubound_loss:
                ubound_loss = ub_loss
                W_best = w
            lbound_loss = max([(w.T*a_i)[0,0]+b_i for (a_i,b_i) in model])+self.regularizer.value(w)
            #assert lbound_loss < ubound_loss
            e_t = ubound_loss-lbound_loss
            #if not self.callbackfun == None:
            #    self.A = W_best
            #    self.callback()
            #e_rel = e_t/ubound_loss
            print "iteration", t
            print ubound_loss
            print lbound_loss
            print "epsilon tolerance:", e_t
            print "termination at", self.e
            print "***********"
        self.resource_pool["iteration_count"] = t
        print self.loss.loss(W_best)+self.regularizer.value(W_best)
        print "norm of learned weight vector", norm(W_best)
        self.A = W_best


    def getModel(self):
        return Model.LinearModelWithBias(self.A, 0.)
        


class L2Regularizer(object):
    
    def __init__(self, lamb):
        assert lamb>0.
        self.lamb = lamb
    
    def value(self, W):
        l2norm = (W.T*W)[0,0]
        return 0.5*self.lamb*l2norm
    
    def gradient(self, W):
        """gradient of 0.5*lamb*|W|*2 is lamb*W"""
        return self.lamb*W
    
