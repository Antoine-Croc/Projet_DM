import requests as re
import random as rd
import os
from bs4 import BeautifulSoup as bs


img_folder_path = "/home/antoine/Documents/Projet_DM/image_tests" 
url = "https://www.4freephotos.com/"
# print(soup.prettify()) pour voir tout le code html 'proprement'


def get_page(page_num):
    page_url = "https://www.4freephotos.com/photos.php?&page={page_n}&order=latest"
    req = re.get(page_url.format(page_n=page_num))
    soup = bs(req.text, 'html.parser')
    return soup

def get_tags(link):
    req = re.get(link)
    soup = bs(req.text, "html.parser")
    for imgtag in soup.find_all("meta", attrs={"name":"keywords"}):
        taglist=imgtag.get("content").split(", ")
    return taglist

def get_n_pics(n):
    page_num = 0
    img_list = []
    img_list2= []
    while len(img_list) < n:
        page_num += 1
        soup = get_page(page_num)
        for img in soup.find_all("img"):
            if img.get("height") and img.get("width"):
                tags=get_tags("https://www.4freephotos.com/" + img.find_parent("a")["href"])
                #print("https://www.4freephotos.com/" + img.find_parent("a")["href"])
                #img_list2.append(img) #<-- list of tags
                img_list.append(jsonify(img,tags)) # list of jsonified_tags
    img_list = img_list[:n]
    return img_list



def jsonify(tag,keywords):
    jsonified_tag = {}
    jsonified_tag["jpglink"] = "https://www.4freephotos.com/" + tag["src"] # To get full link to pictures
    jsonified_tag["height"] = tag["height"]
    jsonified_tag["width"] = tag["width"]
    jsonified_tag["title"] = tag["alt"]
    if tag["height"] > tag["width"]:
        jsonified_tag["orientation"] = "portrait"
    else:
        jsonified_tag["orientation"] = "landscape"
    jsonified_tag["keywords"] = keywords
    return jsonified_tag

def download_to_path(path, url, name):
    r = re.get(url)
    with open(path + "/" + name, "wb") as writer: 
            writer.write(r.content)



img_list = get_n_pics(100)
for img in img_list:
    img_title="{title}.jpg".format(title=img["title"].replace(" ", "_"))
    if os.path.isfile("image_tests/{img_title}".format(img_title=img_title))==False:
        download_to_path(img_folder_path, img["jpglink"], img_title)
    else:
        print("ok")

def random_sample(n, imglist):
    user_list = rd.sample(imglist,n)
    return user_list
    
user_choice = random_sample(15,img_list)

