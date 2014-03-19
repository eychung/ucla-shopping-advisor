import numpy as np
import cPickle
import csv
import itertools
from sklearn.cross_validation import ShuffleSplit, KFold
from rankboost import BipartiteRankBoost
import random
from sklearn.externals.joblib import Parallel, delayed
import sklearn
import features as feat

# features: from loadFeatures
# labels: labels.train
def crossValidation(labels, features, classifier, train_products, test_products, pairwise=False):
	assert pairwise == False

	y_train = [val for idx in train_products for val in labels[idx]]
	X_train = [val for idx in train_products for val in features[idx]]
	classifier = classifier.fit(X_train, y_train)

	X_test = [val for idx in test_products for val in features[idx]]
	P_test = classifier.predict_proba(X_test)[:,1]

	myscore = 0.0
	flatidx = 0
	for idx in test_products:
		myfeatures, mylabels = features[idx], labels[idx]

		ntechattr = len(mylabels)
		ranking = P_test[flatidx:flatidx+ntechattr].argsort()[::-1]
		flatidx += ntechattr

        ranked_labels = [mylabels[rank] for rank in ranking]

        myscore += scoreProduct(ranked_labels)

	return myscore/len(test_products)

# Goes through the each feature (technical attribute) in the list.
def loadFeatures(namelist, mode):
	featurelist = []
	for name in namelist:
		filename = name + '.' + mode
		featurelist.append(cPickle.load(open(filename, 'rb')))
	features = []
	for feats in zip(*featurelist):
		features.append([list(tup) for tup in zip(*feats)])
	return features

# Computes average precision for ranked labels of an author's papers.
def scoreProduct(ranked_labels):
	score = 0.0
	confirmedCount = 0
	for idx, label in enumerate(ranked_labels):
		if label is 1:
			confirmedCount += 1
			score += float(confirmedCount)/float(idx+1)
	score /= ranked_labels.count(1)

	return score

# train_products are the 24 base products acquired from cv_products (using trainlabels)
if __name__ == '__main__':
	classifier = BipartiteRankBoost(n_estimators=50, verbose=1)

	feature_list = feat.userAttributes

	trainfeatures = loadFeatures(feature_list, mode='train')
	trainlabels = cPickle.load(open('labels.train', 'rb'))

	print "train features and train labels set" 
        
	cv_products = KFold(len(trainlabels), n_folds=5, indices=True, shuffle=True, random_state=1)
	for train_products, test_products in cv_products:
		print train_products
    
	score = Parallel(n_jobs=-1)(delayed(crossValidation)(trainlabels, trainfeatures, classifier, train_products, test_products, pairwise=False) for train_products, test_products in cv_products)

	score = np.array(score)
	print 'score mean, std, mean-std:', score.mean(), score.std(), score.mean() - score.std()














