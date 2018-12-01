from pymongo import MongoClient,ASCENDING, DESCENDING

def connect():
    client=MongoClient("mongodb://TsungJui:s3353830@toc-shard-00-00-nmnfw.mongodb.net:27017,toc-shard-00-01-nmnfw.mongodb.net:27017,toc-shard-00-02-nmnfw.mongodb.net:27017/region?ssl=true&replicaSet=TOC-shard-0&authSource=admin&retryWrites=true")
    return client

def getAllNames(col):
    # Project all names field of docs in the collection
    names=col.find({}, {"name":1 , "_id":0 })
    li=[]
    for name in names:
        li.append(name.get("name"))
    return li

def getAllNamesOfCertainType(col,requestType):
    names=col.find({"type":requestType},{"name":1,"_id":0}) # find the restaurant with certain type
    return names

def getFB(col,name):
    fbCursor=col.find({"name": name},{"url":1 , "_id":0} )
    return fbCursor[0].get("url")

def getAddress(col,name):
    addressCursor=col.find({"name": name},{"address":1 , "_id":0})
    return addressCursor[0].get("address")
def getPhoneNumber(col,name):
    phoneCursor=col.find({"name": name},{"contact info":1 , "_id":0} )
    return phoneCursor[0].get("contact info")
def getMap(col,name):
    mapCursor=col.find({"name": name},{"mapURL":1 , "_id":0} )
    return mapCursor[0].get("mapURL")
def getBussinessHour(col,name):
    hourCursor=col.find({"name": name},{"bussiness hour":1 , "_id":0} )
    return hourCursor[0].get("bussiness hour")