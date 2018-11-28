import os
from bs4 import BeautifulSoup
import requests
from .scraper1 import requestfb
import pprint

urlToRequest1=[

    {
        "url": "https://www.facebook.com/pages/%E8%90%AC%E5%AE%A2%E6%A8%93/105752952832134",
        "type": [u"中式小吃"]
    },
    {
        "url": "https://www.facebook.com/pages/%E8%8A%B1%E8%AA%9E%E9%90%B5%E6%9D%BF%E7%87%92/183773784986690",
        "type": [u"鐵板燒"]
    },
    {
        "url" : "https://www.facebook.com/pages/%E5%BB%A3%E8%B6%8A%E7%BE%8E%E9%A3%9F%E5%BA%97/159076434158893",
        "type": [u"越南料理"]
    },
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
        # print(commentsoup.prettify())
        # print(commentsoup.prettify())
        dictForOnePage["address"]=commentsoup.find(class_="uiList _4kg").string
        dictForOnePage["contact info"]=commentsoup.find(findcontact).string
        # get date info
        try:
            timelist=[]
            # find time container
            timeContainer=commentsoup.find("tr",id="vertex-info-item-hours")
            times=timeContainer.find_all("tr")
            for time in times:
                weekday=time.contents[0].string
                bussinessHour=time.contents[1].string
                if weekday is None:
                    try: 
                        tmp=timelist.pop()
                        tmp=f"{tmp}, {bussinessHour}" 
                        timelist.append(tmp)
                    except IndexError as e: # this is the first element
                        timelist.append(f"{bussinessHour}")
                else:
                    hourstring=f"{weekday} {bussinessHour}"
                    timelist.append(hourstring)
            dictForOnePage["bussiness hour"]=timelist
        except AttributeError as e: # for safety
            dictForOnePage["bussiness hour"]=[]
        ###############

        # get mapURL
        mapURLContainer=commentsoup.find(id="vertex-info-item-address")
        if mapURLContainer: # not None
            link=mapURLContainer.find("td",class_="_480u")
            dictForOnePage["mapURL"]=link.a.attrs.get("href","lll") # get mapURL
    return dictForOnePage



# if __name__ == "__main__":
#     result=[]
#     pp=pprint.PrettyPrinter(indent=4,width=100)
#     for urlItem in urlToRequest1:
#         data=parsing2(urlItem)
#         data["url"]=urlItem.get("url")
#         data["type"]=urlItem.get("type")
#         result.append(data)
#     for item in result:
#         pp.pprint(item)
#         print("\r\n")
    
