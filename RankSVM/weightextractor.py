# Extracts the feature weights from the learned model (stored in a pickled Python object) and stores them in a text file

import numpy as np
import cPickle
f = open('model.pckl', 'rb')
model = cPickle.load(f)
f.close()
W = model.W
np.savetxt('./coefficients/coeffnode54.txt', W)
