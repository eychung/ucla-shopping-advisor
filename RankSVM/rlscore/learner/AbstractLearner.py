from .. import DataSources


class RLS(object):
    '''RLS learner module.'''
    
    
    def createLearner(cls, **kwargs):
        learner = cls()
        learner.setResourcePool(kwargs)
        learner.loadResources()
        return learner
    createLearner = classmethod(createLearner)
    
    
    def setResourcePool(self, rp):
        """
        Sets the resource pool for the learner.
        
        @param rp: container of resources from which the learner infers the concept to be learned.
        @type rp: dict
        """
        self.resource_pool = rp
    
    
    def loadResources(self):
        """
        Loads the resources from the previously set ResourcePool object.
        
        @raise Exception: when some of the resources required by the learner is not available in the ResourcePool object.
        """
        #self.parameters = params
        #self.setParameters(params)
        
    
    
    def requiredResources(self):
        """
        Returns the names of the DataSources corresponding to the resources required by the learner.
        
        @return: a list of class names of the subclasses of the DataSource class.
        @rtype: list
        """
        
        names = []
        return names
    
    
    def getResourcePool(self):
        """
        Returns the ResourcePool object of the learner.
        
        @return: container of resources from which the learner infers the concept to be learned.
        @rtype: dict
        """
        return self.resource_pool
    
    
    def supportsModelSelection(self):
        """Returns whether the learner supports model selection.
        
        @return: whether the learner supports model selection
        @rtype: boolean"""
        return False
        
    
    def train(self):
        """Trains a predictor"""
        pass
    
    
    def getModel(self):
        raise Exception("AbstractLearner does not have an implemented getModel function.")

