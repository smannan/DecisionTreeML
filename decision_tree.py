
import copy
import math
import sys

from collections import OrderedDict

THRESH = 0.0

# read data from a comma-seperated text file
# first line is header giving attribute names
# last item in each row is the class for that row
# returns a list of attributes, labels,
# and a numpy array of data

def read_input(filename):
	f = open(filename,'r').read().split('\n')
	attributes = f[0].split(',')

	labels = []
	data = []
	for line in f[1:]:
		line = line.split(',')
		feat = OrderedDict()
		for item in zip(attributes, line[:-1]):
			feat[item[0]] = item[1]

		data.append((line[-1], feat))

	return (data)

class Tree:
		def __init__(self, label):
			self.label = label
			self.children = []

class ML:
	def __init__(self):
		self.root = Tree("root")

	def post_traversal(self, T, space):
		if T:
			print ('{0}{1}'.format(' '.join([''] * space), T.label))
			for child in T.children:
				self.post_traversal(child, space + 4)	

	# return the majority class found in D
	# D is a 1-dim list of classes
	def find_majority_class(self, D):
		counts = {}
		max_count = 1
		majority = 0

		for item in D:
			if item[0] in counts:
				counts[item[0]] += 1
			else:
				counts[item[0]] = 1

		for key in counts.keys():
			if counts[key] > max_count:
				majority = key
				max_count = counts[key]

		return majority

	# compute entropy of a dataset
	def entropy(self, D):
		entropy = 0
		counts = {}

		for row in D:
			if row[0]in counts:
				counts[row[0]] += 1
			else:
				counts[row[0]] = 1

		num_labels = len(D)
		for label in counts.keys():
			val = float(counts[label]) / num_labels
			entropy += -(val * math.log(val, 2))

		return entropy

	# index = which attribute to partition 
	# data on
	# N = # of possible values the attribute 
	# can take
	# returns a {}
	# key = attribute value
	# value = list of labels
	def partition_data(self, D, index):
		partition = {}
		split = {}

		for i in range(len(D)):
			row = D[i][1]
			attr = row[row.keys()[index]]

			if attr in partition:
				partition[attr].append(D[i][0])
				split[attr].append((D[i][0], row))

			else:
				partition[attr] = []
				partition[attr].append(D[i][0])

				split[attr] = []
				split[attr].append((D[i][0], row))

		return partition, split

	# determine the level of impurity
	# that would result from splitting
	# the data on attribute A
	def impurity_eval(self, D, index):
		impurity = 0
		num_samples = float(len(D))
		partition, split = self.partition_data(D, index)

		for key in partition.keys():
			impurity += len(partition[key]) / num_samples * \
				self.entropy(partition[key])

		return impurity, split

	# determine if the data has just one class
	def same_class(self, D):
		classes = set()
		
		for row in D:
			classes.add(row[0])
		
		return len(classes) == 1

	# Implements the decision tree algo
	# D = tuple of (labels, features)
	# features = nxp numpy array where
	# n = number of samples and p = number of 
	# attributes
	# A = list of attributes
	# T = tree node
	def decision_tree(self, D, T):
		# if all samples are of the same class, return
		if (self.same_class(D)):
			return Tree(str(D[0][0]))

		# if the attribute list is empty
		elif (not D[0][1].keys()):
			return Tree(str(self.find_majority_class(D)))

		else:
			# determine the current level of impurity
			p0 = self.entropy(D)
			max_reduction = 0
			Ag = None
			new_split = None

			# determine impurity level that would 
			# result in splitting on the attribute
			# then choose the attribute that gives
			# the greatest impurity reduction
			attr = D[0][1].keys()
			for i in range(len(attr)):
				pi, split = self.impurity_eval(D, i)
				if p0 - pi > max_reduction:
					max_reduction = p0 - pi
					Ag = attr[i]
					new_split = split

			# if the impurity reduction is not 
			# greater than some threshold,
			# return the majority class
			if max_reduction < THRESH:
				return Tree(str(self.find_majority_class(D)))

			# can further reduce impurity within samples
			else:
				feat = new_split.keys()
				Tg = Tree(str(Ag))
				T.children.append(Tg)

				for key, split in new_split.items():
					for row in split:
						row[1].pop(Ag, None)

				for f in feat:
					Dj = new_split[f]
					if (Dj):
						Tf = Tree(str(f))
						T_new = self.decision_tree(Dj, Tf)
						Tf.children.append(T_new)
						Tg.children.append(Tf)
				return Tg

	def train(self, D):
		self.decision_tree(D, self.root)

	def classify(self, feature, root):
		# print ('On node {0}'.format(root.label))

		if not root.children:
			# print ('returning label {0}'.format(root.label))
			return (root.label)

		else:
			for child in root.children:
				# print ('Child {0}'.format(child.label))
				if child.label in feature and child.children:
					for grandchild in child.children:
						if feature[child.label] == grandchild.label:
							# print ('Moving to node {0}'.format(grandchild.label))
							return self.classify(feature, grandchild)
				else:
					# print ('returning label {0}'.format(child.label))
					return (child.label)

	def accuracy(self, D):
	   total = float(len(D))
	   count = 0.0
	   for row in D:
	      pred = self.classify(row[1], self.root)
	      if row[0] == pred:
	         count= count+1.0
	   return count/total
	
	def getStats(self, classification, D):
	   tpCount = 0.0
	   tnCount = 0.0
	   fpCount = 0.0
	   fnCount = 0.0
	   for row in D:
	      pred = self.classify(row[1], self.root)
	      if pred == classification:
	         #classified positive
	         if row[0] == classification:
	            #actual positive
	            tpCount = tpCount + 1.0
	         else:
	            #actual negative
	            fpCount = fpCount + 1.0
	      else:
	         #classified negative
	         if row[0] == classification:
	            #actual positive
	            fnCount = fnCount + 1.0
	         else:
	            #actual negative
	            tnCount = tnCount + 1.0
	            return tpCount, tnCount, fpCount, fnCount

	def getF1(self, tp, tn, fp, fn):
	   precision = tp / (tp + fp)
	   recall = tp / (tp + fn)
	   f1Score = (2.0 * precision * recall) / (precision + recall)
	   return f1Score

# test filename = test_data.txt
def main():
	filename = sys.argv[1:][0]
	tree = ML()
	D = read_input(filename)
	tree.train(D)
	tree.post_traversal(tree.root, 0)
	test = {'Age':'young','Has_job':'true','Own_house':'false','Credit_rating':'false'}
	pred = tree.classify(test, tree.root)
	print ("Predicted {0} for {1}".format(pred, test))
	#print (tree.)

if __name__ == "__main__":
	main()
























