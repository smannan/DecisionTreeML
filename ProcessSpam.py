#!/usr/local/bin/python3
from __future__ import unicode_literals
#import decision_tree
#import NaiveBayes
import ML
import sys
from collections import OrderedDict
import os
import re
import random
import json

class ProcessSpam:

   def __init__(self):
      self.topwords = 20

      self.titleVocab = set()
      self.textVocab = set()
      self.languages = set()
      self.allUsers = set() 

      self.entities = {}
      self.documents = []
      self.features = []

      self.stopwords = set(['the', 'of', 'and', 'to', 'a', 'in', \
       'that', 'is', 'was', 'he', 'for', 'it', 'with', 'as', 'his' \
       'on', 'be', 'at', 'by', 'i', 'you', 'an', 'your'])

   # count number of posts written by a user
   def getPostCount(self, uid, allPosts):
      count = 0

      for post in allPosts:
         if post["author_id"] == uid:
            count = count + 1

      return count

   # parse a post for title and text
   # content, language, and users
   def parse_post(self, post, entId, uid, titles, text, data):   
      if entId not in titles:
         titles[entId] = ''
                  
      if entId not in text: 
         text[entId] = ''
                  
      titles[entId] += post["title"]
      text[entId] += post["text"]
      
      self.languages.add(post["language"])
      self.allUsers.add(uid)

      data.append((str(entId), post)) 

   # returns a list tuples (entity, post)
   def getPostsByTopEntities(self, dirName, potName):
      
      contentFile = open(dirName + '/' + potName + '-content.json', 'r')
      content = json.load(contentFile)
      
      usersFile = open(dirName + '/' + potName + '-user.json', 'r')
      users = json.load(usersFile)
      
      data = []
      titles = {}
      text = {}  

      for entity in self.entities:
         # each entity has a list of user ids
         for uid in entity["user_ids"]:
            
            # go through all the content
            for post in content:
            
               # if the post was written by the user
               # add the post text, title, language, and 
               # user id to all users    
               if post["author_id"] == uid:
                  self.parse_post(post, entity["id"], uid, titles, text, data)
      
      # create a vocabulary for top words 
      # in titles for each entity
      for entity in titles.keys():
         for word in set(self.parseTextBlock(titles[entity], \
          self.topwords)): self.titleVocab.add(word)
      
      # create a vocabulary for top words
      # in content for each entity
      for entity in text.keys():
         for word in set(self.parseTextBlock(text[entity], self.topwords)):
            self.textVocab.add(word)
      
      self.documents = data
      return data  
      
   # return entities with the most posts
   def getTopEntities(self, count, dirName, potName):
      print ("getting entities")
      result = []
      contentFile = open(dirName + '/' + potName + '-content.json', 'r')
      content = json.load(contentFile)
      
      entitiesFile = open(dirName + '/' + potName + '-entities.json', 'r')
      entities = json.load(entitiesFile)
      
      
      entPostCounts = {}
      for entity in entities:
         entPostCounts[str(entity["id"])] = 0
      
         # for all users, count number of posts per user
         # then update count for the entity   
         for uid in entity["user_ids"]:
            numPosts = self.getPostCount(uid, content)
            entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts
      
      # get top 20 entities
      values = sorted([(v, k) for (k, v) in entPostCounts.items()], reverse=True)
      for val in values[:count]:
         result.append(entities[int(val[1])])
      
      self.entities = result

      return result
      
   # given a list of words
   # return the top n words
   def getNCommonWords(self, words, n):
      wordCounts = {}
      for word in words:
         if word and word not in self.stopwords:
            if word in wordCounts:
               wordCounts[word] += 1
            else:
               wordCounts[word] = 1
      
      wordCounts = sorted([(v, k) for (k, v) in wordCounts.items()], reverse=True)
      wordCounts = [v[1] for v in wordCounts[:n]]
      return set(wordCounts)

   # given a string, remove punctuation
   # convert to lowercase
   # and return the top numWords
   def parseTextBlock(self, data, numWords):
      data = re.sub(r'[\.;:,\-!\?]', r'', data)
      data = data.lower()
      return self.getNCommonWords(data.split(' '), numWords)

   # returns one feature
   # ordered dict with key = attributes 
   # and values = attribute values
   def getFeatures(self, docType, record):
      processedRecord = OrderedDict()
      
      if docType == "content":
         for author in self.allUsers:
            colName = "author_id_" + str(author)
            processedRecord[colName] = 1 if author == record["author_id"] else 0
         
         # titleWords = self.parseTextBlock(record["title"], self.topwords)
         titleWords = re.sub(r'[\.;:,\-!\?]', r'', record["title"]). \
          lower().split(' ')
         
         for word in sorted(self.titleVocab):
            colName = "title_word_" + word
            processedRecord[colName] = titleWords.count(word) if word \
             in titleWords else 0
         
         # textWords = self.parseTextBlock(record["text"], self.topwords)
         textWords = re.sub(r'[\.;:,\-!\?]', r'', record["text"]). \
          lower().split(' ')
         
         for word in sorted(self.textVocab):
            colName = "text_word_" + word
            processedRecord[colName] = textWords.count(word) if word in \
             textWords  else 0
      
      else:
         processedRecord = record

      return processedRecord
      
   # returns a list of tuples (label, feature)
   # where label is an entity and 
   # feature is an ordered dict
   def extractFeatures(self, docs):
      result = []
      i = 1
      
      for val in docs:
         #if i % 200 == 0:
         #   print("%d of %d" % (i, len(docs)))
         #i += 1
         
         result.append((val[0], self.getFeatures("content", val[1])))
      
      self.features = result
      return result

def main():
   # Need honeypot server directory
   args = sys.argv[1:]
   if not args or len(args) < 1: 
      print("usage: ProcessSpam.py filename")
      sys.exit(1)
   
   filename = args[0]
   potName = filename.split('/')[-1]

   
   if os.path.exists(filename) and os.path.exists(filename + "/" + \
    potName + "-content.json"):
      ps = ProcessSpam()
      
      # get top 20 entities
      ps.getTopEntities(20, filename, potName)
      
      # parse vocab for text and title
      ps.getPostsByTopEntities(filename, potName)

      # extract features
      ps.extractFeatures(ps.documents)
      
      # split testing/training
      random.shuffle(ps.features)
      cutoff  = int(len(ps.features) / 3)
      testSet, trainingSet = ps.features[:cutoff ], ps.features[cutoff:]
      
      NB = ML.ML()
      NB.train(trainingSet)
      print (NB.accuracy(testSet))
      tp, tn, fp, fn = NB.getStats(testSet[0][0],testSet)
      print("True positive: {0}\nTrue negative: {1}\nFalse positive: {2}\nFalse negative {3}\n".format(tp, tn, fp, fn))
      
      if(tp > 0):
         print("F1 score: {0}".format(NB.getF1(tp, tn, fp, fn)))
      
      else:
         print("No true positive")
      
      print("done")
   
   else:
      print("directory %s isn't a honeypot directory" % filename)
      sys.exit(1)

if __name__ == '__main__':
  main()
