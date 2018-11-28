def queryURL(urlToRequest,parseFuc):
    result=[]
    for urlItem in urlToRequest:
        data=parseFuc(urlItem)
        data["url"]=urlItem.get("url")
        data["type"]=urlItem.get("type")
        result.append(data)
    return result