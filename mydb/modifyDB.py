import sys
import os
# if we run "python3 modifyDB.py" (run python module like a script)
# sys.path[0] will be the folder containing modifyDB.py
# '/Users/tsungjui/Desktop/ncku/TC/TOC/mydb'
sys.path.insert( 0,os.path.abspath("..") )
print(sys.path)

# ".." here is relative to the directory you're executing from,
# not the directory containing that mydb/modifyDB.py
# print(os.path.abspath(".."))
from pymongo import MongoClient,ASCENDING, DESCENDING
from webscraper import queryURL
from webscraper.scraper1 import urlToRequest,parsing1
from webscraper.scraper2 import urlToRequest1,parsing2
import requests

def connect():
    client=MongoClient("mongodb://TsungJui:s3353830@toc-shard-00-00-nmnfw.mongodb.net:27017,toc-shard-00-01-nmnfw.mongodb.net:27017,toc-shard-00-02-nmnfw.mongodb.net:27017/region?ssl=true&replicaSet=TOC-shard-0&authSource=admin&retryWrites=true")
    return client


def insertDocs(col,dataList):
    writeRe=col.insert_many(dataList)
    return writeRe

def createIndex(col):
    col.create_index("name",unique=True)

if __name__ == "__main__":
    result=queryURL(urlToRequest,parsing1)
    result1=queryURL(urlToRequest1,parsing2)
    client=connect()
    # create a collection
    ncku=client.region.ncku
    createIndex(ncku)
    print(insertDocs(ncku,result).inserted_ids)
    print(insertDocs(ncku,result1).inserted_ids)