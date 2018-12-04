import json
import os
import requests
import sys
# the internal object
from app.stateMachine import userList,typeList
from app.stateMachine.foodAsking import FoodAsking
from app.user import User
from mydb.getFromDB import getAllNames
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
            "text": text,
            "metadata": "{} has been sent!",
        })
    }
    return data


def findUser(psid):
    # if the user is already in a conversation
    for index,user in enumerate(userList):
        if user.psid == psid: # find the user
            return index
    return -1


def resMessages(psid,text):
    print(text)
    accessToken=os.environ.get("ACCESS_TOKEN")
    # if userIndex is -1 -> this user is a new user
    userIndex=findUser(psid)
    
    if userIndex==-1 : # new user!
        currentUser=User(psid)
        userList.append(currentUser)
    else: # get old user
        print("this is an old user")
        currentUser=userList[userIndex]


    if currentUser.foodAsking.is_dummy():  # initial is dummy state, can go to type or name state
        typeFlag=False
        nameFlag=False
        for foodType in typeList:
            if foodType in text: # a certain food type is mentioned in the text
                currentUser.foodAsking.gotoType(foodType) # transition to askingType
                typeCursor=currentUser.foodAsking.allNames
                li=[]
                for item in typeCursor:
                    li.append(item.get("name"))
                currentUser.foodAsking.nameListsBasedOnType=li
                dataTosend=makingHeader(psid, "\n".join(li)) # join all the string name
                typeFlag=True
                break
        
        if not typeFlag: # there is no such request type, maybe user input is a certain restaurant?
            allNameAvailable=getAllNames(currentUser.foodAsking.ncku) # get all documents in db
            for name in allNameAvailable:
                if name in text:
                    currentUser.foodAsking.gotoName() # to name state
                    currentUser.foodAsking.resturantName=text[3:] # get the resturant name
                    nameFlag=True
                    dataTosend=makingHeader(psid,u"想知道什麼資訊？\n(地址,fb網址,聯絡方式,google map網址,營業時間）")
        
        if not typeFlag and not nameFlag:    
            dataTosend=makingHeader(psid,u"你的input錯了喔！\n請輸入想知道+餐廳類型 或是 想知道+餐廳名稱")
    
    elif currentUser.foodAsking.is_askingType(): # user must ask information about the resturant, must go to name state
        currentUser.foodAsking.gotoName()
        
        if text[3:] in currentUser.foodAsking.nameListsBasedOnType: # if the resturant name user wants(想知道xxx)
            currentUser.foodAsking.resturantName=text[3:] # get the resturant name
            dataTosend=makingHeader(psid,u"想知道什麼資訊？\n(地址,fb網址,聯絡方式,google map網址,營業時間）")
        else:
            dataTosend=makingHeader(psid,u"沒有這家餐廳喔！\n請重新輸入想知道+餐廳類型 或是 想知道+餐廳名稱")
            del currentUser.foodAsking.nameListsBasedOnType # erase cuz we request user to reinput
            currentUser.foodAsking.to_dummy() # bad request, force it to dummy state
    else: # in name, address, contact info, google map, hour state
        if u"地址" in text: # asking address
            currentUser.foodAsking.gotoAddress()
            whatUserWant=currentUser.foodAsking.address
        elif u"聯絡方式" in text: # asking contact info
            currentUser.foodAsking.gotoPhoneNumber()
            # print(currentUser.foodAsking.phone)
            if not currentUser.foodAsking.phone:
                whatUserWant=u"我們沒有他們的聯絡方式，抱歉！！！"
            else:
                whatUserWant=currentUser.foodAsking.phone
        elif u"map網址" in text :
            currentUser.foodAsking.gotoMap()
            whatUserWant=currentUser.foodAsking.map
        elif u"營業時間" in text:
            currentUser.foodAsking.gotoBussinessHour()
            whatUserWant=currentUser.foodAsking.hour
        elif u"fb" in text:
            currentUser.foodAsking.gotoFB()
            whatUserWant=currentUser.foodAsking.fb
        elif u"想重新輸入餐廳名字" in text or u"想重新輸入餐廳類型" in text:
            currentUser.foodAsking.to_dummy()
            whatUserWant=u"可以重新輸入了！"
        else: 
            whatUserWant=u"你的request不正確喔，請再試一次！"
        
        dataTosend=makingHeader(psid,whatUserWant)
    # using text to deternmine

    # assign metadata
    print(f"state is {currentUser.foodAsking.state}")
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