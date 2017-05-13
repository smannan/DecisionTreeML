import math
import numpy as np

class ML():
   def __init__(self, alpha=0.05):
      self.alpha = 0.05

   def train(self, features):
      self.labels = list(set([pair[0] for pair in features]))

      # seperate all features by label
      # list of lists, each list contains features for
      # each entity
      seperated = [[list(feat.values()) for label, feat in features \
       if label == cl] for cl in self.labels]
      
      # log prior = proba that a sample will have entity
      # given the entity 
      # % samples that have the entity label
      count_sample = len(features)
      self.log_prior = [np.log(len(i) / count_sample) \
       for i in seperated]

      # added alpha smoothing
      # add alpha to each value in the array
      # to account for entities that have 0 samples
      count = np.array([np.array(i).sum(axis=0) \
       for i in seperated]) + self.alpha 
      
      # ??
      self.feature_log_prob_ = np.log(count / \
       count.sum(axis=1)[np.newaxis].T)

   # compute the log probability vector
   # for all documents
   def predict_log_proba(self, X):
      return (np.sum((self.feature_log_prob_ * list(X.values())), \ 
       axis=1) + self.log_prior)

   # get the index of the largest probability for 
   # each documents and return the label
   def classify(self, X):
      return self.labels[np.argmax(self.predict_log_proba(X))]
      
   def accuracy(self, D):
      total = float(len(D))
      count = 0.0
      
      for row in D:
         pred = self.classify(row[1])
         
         if row[0] == pred:
            count = count + 1.0
      
      return count/total

   def getStats(self, classification, D):
      tpCount = 0.0
      tnCount = 0.0
      fpCount = 0.0
      fnCount = 0.0
      
      for row in D:
         pred = self.classify(row[1])
         if pred == classification:
            if row[0] == classification:
               # actual positive
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
      print(precision, recall)
      f1Score = (2.0 * precision * recall) / (precision + recall)
      
      return f1Score

