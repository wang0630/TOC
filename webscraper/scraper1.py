from bs4 import BeautifulSoup
import requests
import pprint

urlToRequest=[
    {
        "url": "https://www.facebook.com/fatcattoast/",
        "type": [u"早午餐",u"日式料理"]
    },
    { 
        "url": "https://www.facebook.com/%E4%B8%80%E7%95%9D%E7%94%B0%E6%AD%90%E9%A2%A8%E5%B0%8F%E9%A4%A8-139475359452929/",
        "type": [u"義式料理",u"火鍋"],
    },
    {
        "url": "https://www.facebook.com/pages/category/Food-Stand/%E6%B7%BB%E7%A6%8F%E9%BA%B5%E9%A4%A8-204290019596211/",
        "type": [u"中式小吃"]
    },
    {
        "url": "https://www.facebook.com/%E9%BB%91%E8%89%B2%E9%A6%99%E8%95%89-%E5%BA%AD%E5%9C%92%E6%97%A9%E9%A4%90-1448638665410367/",
        "type": [u"早點"]
    },
    {
        "url": "https://www.facebook.com/weikechengda/",
        "type": [u"早午餐"]
    },
    {
        "url": "https://www.facebook.com/goodidea20150810/",
        "type": [u"義式料理"]
    },
    {
        "url": "https://www.facebook.com/busypignckuvictor123/",
        "type": [u"滷味"]
    },   
]




def requestfb(url):
    try:
        # get the whole html file
        r=requests.get(url)
        with open("tmp.html","w") as html:
            html.write(r.text)
    except requests.exceptions.RequestException as e:
        print(e)
        return None  
          
def findContactInfo(tag):
    # src= photo of a telphone
    return (tag.has_attr("class")
            and tag.attrs.get("class")[0]=="_4bl9"
            and tag.previous_sibling
            and tag.previous_sibling.get("class")[0]=="_4bl7"
            and tag.previous_sibling.contents[0].attrs.get("src")=="https://static.xx.fbcdn.net/rsrc.php/v3/yz/r/oXiCJHPgn3c.png"
    )

def findPageType1(taglist,dictForOnePage):
    for item in taglist:
        address=item.find(class_="_2wzd")
        if address: # address
            # If a tag has only one child, and that child is a NavigableString,
            # the child is made available as .string:
            # .string is an obj
            # use unicode() to transform to real string
            dictForOnePage["address"]= str(address.contents[2])
        else:
            if len(item.contents) > 1: # it is bussiness hour
                dictForOnePage["bussiness hour"]=str(item.contents[0].string) 
            else: pass



def parsing1(urlToRequest):
    dictForOnePage={}
    # get html string
    requestfb(urlToRequest["url"])
    with open("tmp.html","r") as html:
        # create soup object
        soup=BeautifulSoup(html,"html.parser")
        
        # find google map tag
        googlemap=soup.find(id="u_0_o")
        if googlemap: # not None
            actualLink=googlemap.find("a")
            try:
                dictForOnePage["mapURL"]=actualLink.attrs.get("href") # get google map url
            except AttributeError as e:
                dictForOnePage["mapURL"]= ""
        
        # find name of the resturant
        nameContainer=soup.find(class_="_2b6h")
        if nameContainer:
            dictForOnePage["name"]=str(nameContainer.string)
        
        # find the info tag
        taglist=soup.find_all(class_="_4bl9")
        if taglist: # not empty list
            findPageType1(taglist,dictForOnePage)
            # appending target name
            dictForOnePage["type"]= urlToRequest["type"]
            # find the phone number
            contact=soup.find(findContactInfo)
            try: # maybe no phone number?
                dictForOnePage["contact info"]= str(contact.string)
            except AttributeError as e:
                dictForOnePage["contact info"]= ""
            return dictForOnePage

# if __name__ == "__main__":
#     result=[]
#     pp=pprint.PrettyPrinter(indent=4,width=60)
#     # for urlItem in urlToRequest:
#     #     result.append(parsing1(urlItem))
#     for urlItem in urlToRequest1:
        
#     for item in result:
#         pp.pprint(item)
#         print("\r\n")
    