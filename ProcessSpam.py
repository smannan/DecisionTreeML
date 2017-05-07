#!/usr/bin/python
from __future__ import unicode_literals
import sys
import os
import re
import random
import json

titleVocab = []
textVocab = []
languages = set() 

def getPostCount(id, allPosts):
   count =0
   for post in allPosts:
      if post["author_id"] == id:
         count = count +1
   return count
   
def getPostsByTopEntities(topEntities, dirName, potName):
   print("getting posts")
   global titleVocab 
   global textVocab 
   global languages
   contentFile = open(dirName +'/'+potName+'-content.json', 'r')
   content = json.load(contentFile)
   usersFile = open(dirName +'/'+potName+'-user.json', 'r')
   users = json.load(usersFile)
   data =[]
   i=0
   for entity in topEntities:
      print(i)
      i=i+1
      uids = [] 
      for user in users:
         if user["ip"] in entity["ips"] and user["uid"] not in uids:
            uids.append(user["uid"])
            for post in content:
               if post["author_id"] == user["uid"]:
                  titleVocab = updateVocabs(post["title"], titleVocab)
                  textVocab = updateVocabs(post["text"], textVocab)
                  languages.add(post["language"])
                  #post = getFeatures("content", post)
                  data.append((str(entity["id"]), post))    
   return data
   
   
   
def getTopEntities(count, dirName, potName):
   result = []
   print("getting entities")
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
   
def getPostsByTopMetaEntities(topEntities, potName):
   print("getting posts")
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
   data = []
   i=0
   for entity in topEntities:
      print(i)
      i=i+1
      for entIp in entity["ips"]:
         uids = []
         for user in usersData[potName]:
            if user["ip"] == entIp and user["uid"] not in uids:
               uids.append(user["uid"])
               for post in contentData[potName]:
                   if post["author_id"] == user["uid"]:
                      post = getFeatures("content", post)
                      data.append((str(entity["id"]), post))       
   #print("%d %d" % (entity["id"], entPostCounts[str(entity["id"])]))  
   return data

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

def parseTextBlock(data):
   data = re.sub(r'[\.;:,\-!\?]', r'', data)
   data = data.lower()
   return list(set(data.split(' ')))

def updateVocabs(data, vocab):
   words = set(parseTextBlock(data))
   allWords = set(vocab) | words
   return list(allWords)
   

def getFeatures(docType, record):
   global titleVocab 
   global textVocab 
   processedRecord = {}
   if docType == "content":
      processedRecord["author_id"] = record["author_id"]
      titleWords = parseTextBlock(record["title"])
      for i in range(0, len(titleVocab)):
         colName = "title_word_" + str(i)
         processedRecord[colName] = 1 if titleVocab[i] in titleWords else 0
      textWords = parseTextBlock(record["text"])
      for i in range(0, len(textVocab)):
         colName = "text_word_" + str(i)
         processedRecord[colName] = 1 if textVocab[i] in textWords else 0
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