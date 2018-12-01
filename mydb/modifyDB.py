import sys
import os
# if we run "python3 modifyDB.py" (run python module like a script)
# sys.path[0] will be the folder containing modifyDB.py
# '/Users/tsungjui/Desktop/ncku/TC/TOC/mydb'
# we force it to look up "..", which is '/Users/tsungjui/Desktop/ncku/TC/TOC' cuz we are in mydb folder
sys.path.insert( 0,os.path.abspath("..") )
print(sys.path)

# ".." here is relative to the directory you're executing from,
# not the directory containing that mydb/modifyDB.py
# print(os.path.abspath(".."))
from pymongo import MongoClient,ASCENDING, DESCENDING
# this line becomes " from /Users/tsungjui/Desktop/ncku/TC/TOC/webscraper import queryURL "
from webscraper import queryURL
from webscraper.scraper1 import urlToRequest,parsing1
from webscraper.scraper2 import urlToRequest1,parsing2
import requests




def insertDocs(col,dataList):
    writeRe=col.insert_many(dataList)
    return writeRe

def createIndex(col):
    col.create_index("name",unique=True)

# if __name__ == "__main__":
#     result=queryURL(urlToRequest,parsing1)
#     result1=queryURL(urlToRequest1,parsing2)
#     client=connect()
#     # create a collection
#     ncku=client.region.ncku
#     createIndex(ncku)
#     print(insertDocs(ncku,result).inserted_ids)
#     print(insertDocs(ncku,result1).inserted_ids)