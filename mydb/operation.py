from pymongo import MongoClient
import requests
def connect():
    client=MongoClient("mongodb://TsungJui:s3353830@toc-shard-00-00-nmnfw.mongodb.net:27017,toc-shard-00-01-nmnfw.mongodb.net:27017,toc-shard-00-02-nmnfw.mongodb.net:27017/region?ssl=true&replicaSet=TOC-shard-0&authSource=admin&retryWrites=true")
    return client


def insertOneDoc(client):
    db=client.region
    db.ncku.insert_one( {
            "name":u"貓吐司堡專賣店",
            "type":[u"日式料理",u"早午餐"],
            "avgPrice": "low",
            "environ": ["indoor"],
            "AC": True,
            "freeDrink":False,
            "freeSoup":False,
            "address": u"台南市東區大學路22巷16-1號",
            "fb": "https://www.facebook.com/fatcattoast/",
            "bussiness hour": "08:30～20:30"
        } )

