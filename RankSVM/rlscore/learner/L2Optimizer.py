'''
Quadratic optimizer for solving the argmin problem within the bundle method loop
for quadratic regularizer.

'''

import cvxopt.solvers
from cvxopt.base import matrix as cm
from cvxopt.base import spmatrix

from scipy.sparse import csr_matrix
from numpy import zeros as numzeros
from numpy import *


    
class PrimalDualOptimizer(object):
    
    #input and output are for the primal problem, but the actual optimization
    #is handled using a dual formulation
    
    def __init__(self, lamb, dimension):
        self.bundle = []
        
        self.bvec = []
        
        self.lamb = lamb
        self.initvals = None
        self.itercount = 0
        
        
    def add_bundle(self, a, b):
        #adds a new linearization to the lower bound that is optimized 
        self.bundle.append(a)
        self.bvec.append(b)
        
        numvar = len(self.bundle)
        if numvar == 1:
            self.P = mat((1./self.lamb)*(a.T*a)[0,0])
            return
        
        newcol = []
        for i in range(numvar):
            a_i = self.bundle[i]
            a_j = a
            val = (1./self.lamb)*(a_i.T*a_j)[0,0]
            newcol.append(val)
        
        newcol = mat(newcol).T
        self.P = vstack((self.P,newcol[0:numvar-1,:].T))
        self.P = hstack((self.P,newcol))
        
            
            
    def optimize(self): 
        
        
        numvar = len(self.bundle)
        
        P = cm(self.P)
        q = cm(- matrix(self.bvec)).T
        
        
        valz = [-1. for x in range(numvar)] + [1. for x in range(numvar)]
        rcoordz = range(numvar) + [numvar for x in range(numvar)]
        ccoordz = range(numvar) + range(numvar)
        
        G = spmatrix(valz, rcoordz, ccoordz)
        h = spmatrix(1., [numvar], [0])
        h = cm(h)
        
        p_dict = cvxopt.solvers.qp(P, q, G=G, h=h)
        #print p_dict['status']
        xx = p_dict['x']
        self.itercount = self.itercount + 1
        print self.itercount
        xx=mat(xx)
        W = csr_matrix(self.bundle[0].shape)
        for i in range(len(self.bundle)):
            W = W+float(-xx[i]/self.lamb)*self.bundle[i]
        return W
    