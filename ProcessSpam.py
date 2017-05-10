#!/usr/bin/python
from __future__ import unicode_literals
import decision_tree
import sys
import os
import re
import random
import json

COMMON_NUM = 5
titleVocab = []
textVocab = []
languages = set()
allUsers = set() 

def getPostCount(id, allPosts):
   count =0
   for post in allPosts:
      if post["author_id"] == id:
         count = count +1
   return count

#def getLabel(doc):
   
   
def getPostsByTopEntities(topEntities, dirName, potName):
   print("getting posts")
   global titleVocab 
   global textVocab 
   global languages
   global allUsers
   contentFile = open(dirName +'/'+potName+'-content.json', 'r')
   content = json.load(contentFile)
   usersFile = open(dirName +'/'+potName+'-user.json', 'r')
   users = json.load(usersFile)
   data =[]
   i=0
   for entity in topEntities:
      print(i)
      i=i+1
      #uids = [] 
      for uid in entity["user_ids"]:
         #uids.append(user["uid"])
         for post in content:
            if post["author_id"] == uid:
               titleVocab = updateVocabs(post["title"], titleVocab)
               textVocab = updateVocabs(post["text"], textVocab)
               languages.add(post["language"])
               allUsers.add(uid)
               #post = getFeatures("content", post)
               data.append((str(entity["id"]), post))    
   return data
   
   
   
def getTopEntities(count, dirName, potName):
   result = []
   print("getting entities")
   contentFile = open(dirName +'/'+potName+'-content.json', 'r')
   content = json.load(contentFile)
   #usersFile = open(dirName +'/'+potName+'-user.json', 'r')
   #users = json.load(usersFile)
   entitiesFile = open(dirName +'/'+potName+'-entities.json', 'r')
   entities = json.load(entitiesFile)
   entPostCounts = {}
   for entity in entities:
      entPostCounts[str(entity["id"])] = 0
      #uids = [] 
      for uid in entity["user_ids"]:
         #if user["ip"] in entity["ips"] and user["uid"] not in uids:
         #uids.append(user["uid"])
         numPosts = getPostCount(uid, content)
         entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts
      print("%d %d" % (entity["id"], entPostCounts[str(entity["id"])]))
   values = sorted([(v, k) for (k, v) in entPostCounts.items()], reverse=True)
   for val in values[:count]:
      result.append(entities[int(val[1])])
   #print(result)
   print([t for t in values[:count]])
   return result
   
   
def getNCommonWords(words, n):
   wordCounts = {}
   for word in words:
      if word in wordCounts:
         wordCounts[word] += 1
      else:
         wordCounts[word] = 1
   wordCounts = sorted([(v, k) for (k, v) in wordCounts.items()], reverse=True)
   wordCounts = [v[1] for v in wordCounts[:n]]
   return wordCounts

def parseTextBlock(data, numWords):
   data = re.sub(r'[\.;:,\-!\?]', r'', data)
   data = data.lower()
   return getNCommonWords(data.split(' '), numWords)
   #return list(set(data.split(' ')))

def updateVocabs(data, vocab):
   words = set(parseTextBlock(data, COMMON_NUM))
   allWords = set(vocab) | words
   return list(allWords)
   

def getFeatures(docType, record):
   global titleVocab 
   global textVocab 
   processedRecord = {}
   if docType == "content":
      processedRecord["author_id"] = str(record["author_id"])
      #processedRecord["title"] = record["title"]
      #processedRecord["text"] = record["text"]
      titleWords = parseTextBlock(record["title"], COMMON_NUM)
      for i in range(0, len(titleVocab)):
         colName = "title_word_" + str(i)
         processedRecord[colName] = "True" if titleVocab[i] in titleWords else "False"
      textWords = parseTextBlock(record["text"], COMMON_NUM)
      for i in range(0, len(textVocab)):
         colName = "text_word_" + str(i)
         processedRecord[colName] = "True" if textVocab[i] in textWords else "False"
   else:
      processedRecord = record
   return processedRecord
   
def extractFeatures(docs):
   result = []
   i=1
   for val in docs:
      if i%200 == 0:
         print("%d of %d" % (i, len(docs)))
      i = i+1
      result.append((val[0], getFeatures("content", val[1])))
   return result

def main():
   global languages
   global allUsers
   global titleVocab 
   global textVocab 
   args = sys.argv[1:]
   if not args or len(args) < 1:
    print("usage: ProcessSpam.py filename")
    sys.exit(1)
   filename = args[0]
   potName = filename.split('/')[-1]
   if os.path.exists(filename) and os.path.exists(filename + "/" + potName+"-content.json"):
      #entities = getTopMetaEntities()
      #allDocs = getPostsByTopMetaEntities(entities, "gjams")
      entities = getTopEntities(20, filename, potName)
      allDocs = getPostsByTopEntities(entities, filename, potName)
      print("cumulative summary")
      print(len(allUsers))
      print(languages)
      print(len(titleVocab))
      print(len(textVocab))
      print("getting features")
      allDocs = extractFeatures(allDocs)
      #print(allDocs[0][1].keys())
      print("got data")
      random.shuffle(allDocs)
      cutoff  = len(allDocs)/3
      print("creating test and training sets")
      testSet, trainingSet = allDocs[:cutoff ], allDocs[cutoff:]
      tree = decision_tree.ML()
      print("training decision tree")
      tree.train(trainingSet)
      #tree.post_traversal(tree.root, 0)
      print("getting accuracy")
      print(tree.accuracy(testSet))
      print("getting f1 score")
      #print(type(testSet[0][0]))
      print(testSet[0][0])
      tp, tn, fp, fn = tree.getStats(testSet[0][0],testSet)
      print(tp, tn, fp, fn)
      if(tp>0):
         print(tree.getF1(tp, tn, fp, fn))
      else:
         print("No true positivex")
      #print(len(testSet))
      #print(len(trainingSet))
      print("done")
   else:
      print("directory %s isn't a honeypot directory" % filename)
      sys.exit(1)
   #usersFile = open('/lib/466/spam/gjams/gjams-user.json', 'r')
   #users = json.load(usersFile)
   #accessFile = open('/lib/466/spam/gjams/gjams-access.json', 'r')
   #access = json.load(accessFile)
   #contentFile = open('/lib/466/spam/gjams/gjams-content.json', 'r')
   #content = json.load(contentFile)
   #entitiesFile = open('/lib/466/spam/gjams/gjams-entities.json', 'r')
   #entities = json.load(entitiesFile)


if __name__ == '__main__':
  main()