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
   
def getTopEntities(count, dirName, potName):
   result = []
   print("getting meta entities")
   contentFile = open(dirName +'/'+potName+'-content.json', 'r')
   content = json.load(contentFile)
   usersFile = open(dirName +'/'+potName+'-user.json', 'r')
   users = json.load(usersFile)
   entitiesFile = open(dirName +'/'+potName+'-entities.json', 'r')
   entities = json.load(entitiesFile)
   entPostCounts = {}
   for entity in entities:
      entPostCounts[str(entity["id"])] = 0
      uids = [] 
      for user in users:
         if user["ip"] in entity["ips"] and user["uid"] not in uids:
            uids.append(user["uid"])
            numPosts = getPostCount(user["uid"], content)
            entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts
      print("%d %d" % (entity["id"], entPostCounts[str(entity["id"])]))
   values = sorted([(v, k) for (k, v) in entPostCounts.items()], reverse=True)
   for val in values[:count]:
      result.append(entities[int(val[1])])
   #print(result)
   print([t for t in values[:count]])
   return result

def getTopMetaEntities():
   result = []
   print("getting meta entities")
   metaFile = open('meta-entities.json', 'r')
   meta = json.load(metaFile)
   gjamsFile = open('/lib/466/spam/gjams/gjams-content.json', 'r')
   gjamsContent = json.load(gjamsFile)
   ggjxFile = open('/lib/466/spam/ggjx/ggjx-content.json', 'r')
   ggjxContent = json.load(ggjxFile)
   npcagentFile = open('/lib/466/spam/npcagent/npcagent-content.json', 'r')
   npcagentContent = json.load(npcagentFile)
   contentData = {"gjams":gjamsContent, "ggjx":ggjxContent, "npcagent":npcagentContent}
   #gjamsFile2 = open('/lib/466/spam/gjams/gjams-entities.json', 'r')
   #gjamsEntities = json.load(gjamsFile2)
   #ggjxFile2 = open('/lib/466/spam/ggjx/ggjx-entities.json', 'r')
   #ggjxEntities = json.load(ggjxFile2)
   #npcagentFile2 = open('/lib/466/spam/npcagent/npcagent-entities.json', 'r')
   #npcagentEntities = json.load(npcagentFile2)
   #entitiesData = {"gjams":gjamsEntities, "ggjx":ggjxEntities, "npcagent":npcagentEntities}
   gjamsFile3 = open('/lib/466/spam/gjams/gjams-user.json', 'r')
   gjamsUsers = json.load(gjamsFile3)
   ggjxFile3 = open('/lib/466/spam/ggjx/ggjx-user.json', 'r')
   ggjxUsers = json.load(ggjxFile3)
   npcagentFile3 = open('/lib/466/spam/npcagent/npcagent-user.json', 'r')
   npcagentUsers = json.load(npcagentFile3)
   usersData = {"gjams":gjamsUsers, "ggjx":ggjxUsers, "npcagent":npcagentUsers}
   pots = ["gjams", "ggjx", "npcagent"]
   entPostCounts = {}
   for entity in meta:
      entPostCounts[str(entity["id"])] = 0
      for entIp in entity["ips"]:
         for potName in pots:
               uids = []
               for user in usersData[potName]:
                  if user["ip"] == entIp and user["uid"] not in uids:
                    uids.append(user["uid"])
                    numPosts = getPostCount(user["uid"], contentData[potName])
                    entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts 
      print("%d %d" % (entity["id"], entPostCounts[str(entity["id"])]))  
   values = sorted([(v, k) for (k, v) in entPostCounts.items()], reverse=True)
   for val in values[:50]:
      result.append(meta[int(val[1])])
   #print(result)
   print([t for t in values[:50]])
   return result


def getTopMetaEntities2():
   result = []
   print("getting meta entities")
   metaFile = open('meta-entities.json', 'r')
   meta = json.load(metaFile)
   gjamsFile = open('/lib/466/spam/gjams/gjams-content.json', 'r')
   gjamsContent = json.load(gjamsFile)
   ggjxFile = open('/lib/466/spam/ggjx/ggjx-content.json', 'r')
   ggjxContent = json.load(ggjxFile)
   npcagentFile = open('/lib/466/spam/npcagent/npcagent-content.json', 'r')
   npcagentContent = json.load(npcagentFile)
   contentData = {"gjams":gjamsContent, "ggjx":ggjxContent, "npcagent":npcagentContent}
   gjamsFile2 = open('gjams-entities-ids.json', 'r')
   gjamsEntities = json.load(gjamsFile2)
   ggjxFile2 = open('ggjx-entities-ids.json', 'r')
   ggjxEntities = json.load(ggjxFile2)
   npcagentFile2 = open('npcagent-entities-ids.json', 'r')
   npcagentEntities = json.load(npcagentFile2)
   entitiesData = {"gjams":gjamsEntities, "ggjx":ggjxEntities, "npcagent":npcagentEntities}
   entPostCounts = {}
   for entity in meta:
      entPostCounts[str(entity["id"])] = 0
      for entId in entity["ent_ids"]:
         idParts = entId.split('_')
         print(entId) 
         for id in entitiesData[idParts[0]][int(idParts[1])]["user_ids"]:
             numPosts = getPostCount(id, contentData[idParts[0]])
             entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts 
      print("%d %d" % (entity["id"], entPostCounts[str(entity["id"])]))
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