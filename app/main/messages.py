import json
import os
import requests

class ResponseDict(dict):
    def __getitem__(self,item):
        # message["matadata"] = message.__getitem__("metadata")
        # message.__getitem__("metadata") =  dict__getitem__(message,"metadata").format(message.get("text"))
        # __getitem__() is only called with [], dict.get() will not call it. 
        return dict.__getitem__(self,item).format(self.get("text")) 

def makingHeader(psid,text):
    data={
        "messaging_type": "MESSAGE_TAG",
        "tag": "BUSINESS_PRODUCTIVITY",
        "recipient": {
            "id": psid
        },
        "message":ResponseDict({
            "text": "hello",
            "metadata": "{} has been sent!",
        })
    }
    return data


def resMessages(psid,text):
    accessToken=os.environ.get("ACCESS_TOKEN")
    dataTosend=makingHeader(psid,text)
    # assign metadata
    dataTosend["message"]["metadata"]=dataTosend["message"]["metadata"]
    param={"access_token":accessToken}
    if(accessToken):
        # request, using json= will encode the dict object for you
        # using params= will concat the param to the end of url as parameters (starts with ?)
        r=requests.post("https://graph.facebook.com/v2.6/me/messages",json=dataTosend,params=param)
       
        # print(r.status_code) # the status code of this post request
        # print(r.headers)      
        # print(r.url)          
    else:
        print("access token not found")