from bs4 import BeautifulSoup
import requests
from scraper1 import requestfb
import pprint

urlToRequest1=[

    {
        "url": "https://www.facebook.com/pages/%E8%90%AC%E5%AE%A2%E6%A8%93/105752952832134",
        "type": [u"中式小吃"]
    },
    {
        "url" : "https://www.facebook.com/pages/%E5%BB%A3%E8%B6%8A%E7%BE%8E%E9%A3%9F%E5%BA%97/159076434158893",
        "type": [u"越南料理"]
    }
]


def findcontact(tag):
    return( tag.previous_sibling
            and tag.previous_sibling.name=="th"
            and tag.previous_sibling.string == u"聯絡電話") 


def parsing2(urlToRequest1):
    dictForOnePage={}
    # get html string
    requestfb(urlToRequest1["url"])
    with open("tmp.html","r") as html:
        # create soup object
        soup=BeautifulSoup(html,"html.parser")
        dictForOnePage["name"]=str(soup.find("span",class_="_2b6h").string)
        # some stuff resides in the comment area
        commenthtml=soup.find(class_="hidden_elem").contents[0].contents[0]
        # create a soup for this comment html
        commentsoup=BeautifulSoup(commenthtml,"html.parser")
        dictForOnePage["address"]=commentsoup.find(class_="uiList _4kg").string
        dictForOnePage["contact info"]=commentsoup.find(findcontact).string
        date= commentsoup.find(class_="day days").string
        times= commentsoup.find(class_="times").string
        dictForOnePage["bussiness hour"]=f"{date} {times}"
        
    return dictForOnePage
if __name__ == "__main__":
    result=[]
    pp=pprint.PrettyPrinter(indent=4,width=60)
    for urlItem in urlToRequest1:
        data=parsing2(urlItem)
        data["url"]=urlItem.get("url")
        data["type"]=urlItem["type"]
        result.append(data)
    for item in result:
        pp.pprint(item)
        print("\r\n")
    
