
import math
import numpy as np
import sys

THRESH = 0.3

class Tree:
	def __init__(self, label):
		self.label = label
		self.children = []

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
		data.append(line[:-1])
		labels.append(line[-1])

	return (attributes, labels, np.array(data))

# return the majority class found in D
# D is a 1-dim list of classes
def find_majority_class(D):
	counts = {}
	max_count = 1
	majority = 0

	for item in D:
		if item in counts:
			D[item] += 1
		else:
			D[item] = 1

	for key in counts.keys():
		if counts[key] > max_count:
			majority = key
			max_count = counts[key]

	return majority

# compute entropy of a dataset
def entropy(D):
	entropy = 0
	counts = {}

	for label in D:
		if label in counts:
			counts[label] += 1
		else:
			counts[label] = 1

	num_labels = len(D)
	for label in counts.keys():
		val = float(counts[label]) / num_labels
		entropy += -(val * math.log(val, 2))

	return entropy

def partition_data(D, index):
	features = D[1]
	labels = D[0]
	attr_vals = set(features[:,index])
	partition = {}

	for i in range(features.shape[0]):
		row = features[i,:]
		attr = row[index]
		if attr in partition:
			partition[attr].append(labels[i])
		else:
			partition[attr] = []
			partition[attr].append(labels[i])

	return partition

# determine the level of impurity
# that would result from splitting
# the data on attribute A
def impurity_eval(D, index):
	impurity = 0
	num_samples = float(D[1].shape[0])
	partition = partition_data(D, index)

	for key in partition.keys():
		impurity += len(partition[key]) / num_samples * \
			entropy(partition[key])

	return impurity, partition

# Implements the decision tree algo
# D = tuple of (labels, features)
# features = nxp numpy array where
# n = number of samples and p = number of 
# attributes
# A = list of attributes
# T = tree node
def decisionTree(D, A, T):
	# if all samples are of the same class, return
	if (len(set(D[0])) == 1):
		return Tree(D[0][0])

	# if the attribute list is empty
	elif (len(A) == 0):
		return Tree(find_majority_class(D[0]))

	else:
		# determine the current level of impurity
		p0 = entropy(D[0])
		max_reduction = 0
		Ag = None

		# determine impurity level that would 
		# result in splitting on the attribute
		# then choose the attribute that gives
		# the greatest impurity reduction
		num_attr = D[1].shape[1]
		for i in range(num_attr):
			pi, partition = impurity_eval(D, i)
			if p0 - pi > max_reduction:
				max_reduction = p0 - pi
				Ag = i

		# if the impurity reduction is not 
		# greater than some threshold,
		# return the majority class
		if max_reduction < THRESH:
			return Tree(find_majority_class(D[0]))

		# can further reduce impurity within samples
		else:
			T_new = Tree(Ag)

def main():
	filename = sys.argv[1:][0]
	attr, labels, features = read_input(filename)
	D = (labels, features)

if __name__ == "__main__":
	main()
























