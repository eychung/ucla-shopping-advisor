import numpy
from numpy import array
from scipy import sparse
import operator
import ranktree 

class SparseRankSVMLoss(object):
    #nlog(n) time implementation for learning with general utility scores
    #for sparse data
    #supports queries
    
    def __init__(self, X, Y, qids=None):
        X = sparse.csc_matrix(X)
        self.X_csc = X.tocsc()
        self.X_csr = X.tocsr()
        self.Y = array(Y).reshape(Y.shape[0],)
        self.qids = qids
        if self.qids != None:
            self.pairs = []
            for q in qids:
                Y_sub = self.Y[q]
                self.pairs.append(countPairs(Y_sub))
            self.pcount=sum(self.pairs)
        else:
            self.pcount = countPairs(Y)
        
    def loss(self, W):
        F = self.X_csc.T * W
        tsize = F.shape[0]
        F_l = numpy.array(F.T).reshape(tsize,)
        if self.qids == None:
            return self.queryloss(F_l, self.Y)/self.pcount
        else:
            loss = 0.
            iter = 0
            for q, pairs in zip(self.qids, self.pairs):
                if pairs != 0:
                    F_sub = F_l[q]
                    S_sub = self.Y[q]
                    loss += (self.queryloss(F_sub, S_sub))
            loss/=self.pcount
            return loss
    
    def queryloss(self, F_l, S):
        tsize = F_l.shape[0]
        P = [(x, y) for y, x in enumerate(F_l)]
        P.sort(key=operator.itemgetter(0))
        P = [x[1] for x in P]
        cd = ranktree.rank_freq(S, F_l, P, 2 * tsize)
        c = cd[:tsize]
        d = cd[tsize:]
        assert sum(c) == sum(d)
        c_d = c - d
        F_l = numpy.mat(F_l.reshape(F_l.shape[0],1))
        l = (F_l.T * numpy.mat(c_d).T)[0, 0] + sum(c)
        return l
    
    
    def loss_gradient(self, W):
        F = self.X_csc.T * W
        tsize = F.shape[0]
        #When iterating over data structures, list
        #access is much more efficient than numpy array access
        F_l = numpy.array(F.T).reshape(tsize,)   
        S = self.Y
        if self.qids == None:
            l, c_d = self.loss_gradient_query(F_l, S)
            G = self.X_csr * c_d.T
            return l/self.pcount, G/self.pcount
        else:
            l = 0.
            cds = []
            for q, pairs in zip(self.qids, self.pairs):
                if pairs != 0:
                    F_sub = F_l[q]
                    S_sub = S[q]
                    lu, c_d = self.loss_gradient_query(F_sub, S_sub)
                    l += lu
                    cds.append(c_d)
                else:
                    cds.append(numpy.mat(numpy.zeros((1, len(q)))))
            c_d = numpy.mat(numpy.hstack(cds))
            G = self.X_csr * c_d.T
            l /= self.pcount
            G /= self.pcount
            return l,G
        
    def loss_gradient_query(self, F_l, S):
        tsize = F_l.shape[0]
        P = [(x, y) for y, x in enumerate(F_l)]
        P.sort(key=operator.itemgetter(0))
        P = [x[1] for x in P]
        cd = ranktree.rank_freq(S, F_l, P, 2 * tsize)
        c = cd[:tsize]
        d = cd[tsize:]
        assert sum(c) == sum(d)
        c_d = numpy.mat(c - d)
        F_l = numpy.mat(F_l.reshape(F_l.shape[0],1))
        l = (F_l.T * c_d.T)[0, 0] + sum(c)
        return l, c_d
    
class DenseRankSVMLoss(object):
    #nlog(n) time implementation for learning with general utility scores
    #for dense data
    #supports queries
    
    def __init__(self, X, Y, qids=None):
        #self.X = X.todense()
        self.X = X
        self.Y = array(Y).reshape(Y.shape[0],)
        self.qids = qids
        if self.qids != None:
            self.pairs = []
            for q in qids:
                Y_sub = self.Y[q]
                self.pairs.append(countPairs(Y_sub))
            self.pcount=sum(self.pairs)
        else:
            self.pcount = countPairs(Y)
        
    def loss(self, W):
        F = self.X.T * W
        tsize = F.shape[0]
        F_l = numpy.array(F.T).reshape(tsize,)
        if self.qids == None:
            return self.queryloss(F_l, self.Y)/self.pcount
        else:
            loss = 0.
            iter = 0
            for q, pairs in zip(self.qids, self.pairs):
                if pairs != 0:
                    F_sub = F_l[q]
                    S_sub = self.Y[q]
                    loss += (self.queryloss(F_sub, S_sub))
            loss/=self.pcount
            return loss
    
    def queryloss(self, F_l, S):
        tsize = F_l.shape[0]
        P = [(x, y) for y, x in enumerate(F_l)]
        P.sort(key=operator.itemgetter(0))
        P = [x[1] for x in P]
        cd = ranktree.rank_freq(S, F_l, P, 2 * tsize)
        c = cd[:tsize]
        d = cd[tsize:]
        assert sum(c) == sum(d)
        c_d = c - d
        F_l = numpy.mat(F_l.reshape(F_l.shape[0],1))
        l = (F_l.T * numpy.mat(c_d).T)[0, 0] + sum(c)
        return l
    
    
    def loss_gradient(self, W):
        F = self.X.T * W
        tsize = F.shape[0]
        #When iterating over data structures, list
        #access is much more efficient than numpy array access
        F_l = numpy.array(F.T).reshape(tsize,)   
        S = self.Y
        if self.qids == None:
            l, c_d = self.loss_gradient_query(F_l, S)
            G = self.X * c_d.T
            return l/self.pcount, G/self.pcount
        else:
            l = 0.
            cds = []
            for q, pairs in zip(self.qids, self.pairs):
                if pairs != 0:
                    F_sub = F_l[q]
                    S_sub = S[q]
                    lu, c_d = self.loss_gradient_query(F_sub, S_sub)
                    l += lu
                    cds.append(c_d)
                else:
                    cds.append(numpy.mat(numpy.zeros((1, len(q)))))
            c_d = numpy.mat(numpy.hstack(cds))
            G = self.X * c_d.T
            l /= self.pcount
            G /= self.pcount
            return l,G
        
    def loss_gradient_query(self, F_l, S):
        tsize = F_l.shape[0]
        P = [(x, y) for y, x in enumerate(F_l)]
        P.sort(key=operator.itemgetter(0))
        P = [x[1] for x in P]
        cd = ranktree.rank_freq(S, F_l, P, 2 * tsize)
        c = cd[:tsize]
        d = cd[tsize:]
        assert sum(c) == sum(d)
        c_d = numpy.mat(c - d)
        F_l = numpy.mat(F_l.reshape(F_l.shape[0],1))
        l = (F_l.T * c_d.T)[0, 0] + sum(c)
        return l, c_d 
              
def countPairs(Y):
    #n*log(n) algorithm for computing number of pairs
    #Used to compute the normalizer of the empirical risk
    S = Y[:]
    S.sort()
    pairs = 0
    c_ties = 0
    for i in range(1, len(S)):
        if S[i] != S[i-1]:
            c_ties = 0
        else:
            c_ties += 1
        #this example forms a pair with each previous example, that has a lower value
        pairs += i-c_ties
    return pairs 

def countPairs2(Y):
    #Naive implementations of count pairs
    pairs = 0
    for i in range(len(Y)-1):
        for j in range(i+1, len(Y)):
            if Y[i]!= Y[j]:
                pairs += 1
    return pairs
