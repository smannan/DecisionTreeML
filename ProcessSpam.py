#!/usr/bin/python
import sys
import json

def getPostCount(id, allPosts):
   count =0
   for post in allPosts:
      if post["author_id"] == id:
         count = count +1
   return count

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
   gjamsFile2 = open('/lib/466/spam/gjams/gjams-entities.json', 'r')
   gjamsEntities = json.load(gjamsFile2)
   ggjxFile2 = open('/lib/466/spam/ggjx/ggjx-entities.json', 'r')
   ggjxEntities = json.load(ggjxFile2)
   npcagentFile2 = open('/lib/466/spam/npcagent/npcagent-entities.json', 'r')
   npcagentEntities = json.load(npcagentFile2)
   entitiesData = {"gjams":gjamsEntities, "ggjx":ggjxEntities, "npcagent":npcagentEntities}
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
         #idParts = entId.split('_')
         for potName in pots:
            uids =[]
            for user in usersData[potName]:
               if user["ip"] == entIp and user["uid"] not in uids:
                 uids.append(user["uid"])
            for uid in uids:
               numPosts = getPostCount(uid, contentData[potName])
               entPostCounts[str(entity["id"])] = entPostCounts[str(entity["id"])] + numPosts 
      print(entPostCounts[str(entity["id"])])
   return result

def getFeatures(docType, record):
   processedRecord = record
   return processedRecord

def main():
   args = sys.argv[1:]
   if not args or len(args) < 1:
    print("usage: ProcessSpam.py filename")
    sys.exit(1)
   filename = args[0]
   entities = getTopMetaEntities()
   
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