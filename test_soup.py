import requests as re
from bs4 import BeautifulSoup as bs

url = "https://www.4freephotos.com/Gibraltar-rock-fortress-7201.html"
req = re.get(url)
soup = bs(req.text, "html.parser")
print(soup.prettify)


#linklist = []
# #for img in soup.find_all("a"):
#  #   if img.get("href") and img.get("title"):
# for img in soup.find_all("img"):
#     if img.get("height") and img.get("width"):  
#         #print(img.find_parent("a"))
#         linklist.append("https://www.4freephotos.com/" + img.get("href"))
# #print(linklist)


def get_tags(link):
    req = re.get(link)
    soup = bs(req.text, "html.parser")
    for imgtag in soup.find_all("meta", attrs={"name":"keywords"}):
        taglist=imgtag.get("content").split(", ")
        print(imgtag.get("content").split(", "))
    
    return taglist
