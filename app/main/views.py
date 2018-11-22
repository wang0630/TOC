from . import main # import mainBlueprint
from .messages import resMessages
from flask import request
VTOKEN="webhook verify!!!!"

@main.route('/',methods=["GET"])
def index():
    verifyDict=request.args # get parameter in URL
    verifyToken=verifyDict.get("hub.verify_token")
    verifyChallange=verifyDict.get("hub.challenge")
    verifyMode=verifyDict.get("hub.mode")

    if verifyMode=="subscribe" and verifyToken==VTOKEN:
        print("Successful!")
        return verifyChallange
    else: 
        return f"get"

@main.route('/',methods=["POST"])
def index1():
    # parse data as json format
    data=request.get_json()
    entries=data.get("entry") # a list
    # print(data)
    if(data.get("object") == "page"):
        for entry in entries: # entry is the dictionary containing all info
            if "messaging" in entry : # messages_?? event
                messaging=entry["messaging"][0]
                sender=messaging["sender"]["id"]
                if "read" in messaging: # message_reads event:
                    print(f"Message sent to { sender } has been read!")
                elif "delivery" in messaging: # message_delivery event
                    print(f"Message has been delivered by {sender}!")
                else:
                    message=messaging.get("message")
                    if "is_echo" in message: # message_echos event
                        print(message.get("metadata"))
                    else: # message event, make a reply 
                        resMessages(str(sender),message.get("text"))
    return f"post",200