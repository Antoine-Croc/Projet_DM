import requests as re
import random as rd
import os
from bs4 import BeautifulSoup as bs

from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plot
import colr
from sklearn.cluster import KMeans




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



def jsonify(tag,keywords): #créer liste sous format json
    jsonified_tag = {}
    jsonified_tag["jpglink"] = "https://www.4freephotos.com/" + tag["src"] # To get full link to pictures
    jsonified_tag["height"] = tag["height"]
    jsonified_tag["width"] = tag["width"]
    jsonified_tag["title"] = tag["alt"].replace(" ", "_")
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

#------------------------------------------------------ recup couleurs

basic_colors = {
  "white": [255, 255, 255],
  "black": [0, 0, 0],
  "red": [255, 0, 0],
  "green": [0, 255, 0],
  "blue": [0, 0, 255],
  "yellow": [255,255,0],
  "cyan": [0,255,255],
  "magenta": [255,0,255],
  "gray": [128,128,128],
  "orange": [255, 128, 0],
  "purple": [128, 0, 255],
  "pink": [255, 0, 128],
  "brown": [165,42,42],
}

def add_to_list(rgb_list, tint):
  output = []
  for i in rgb_list:
    if tint == "dark":
    # Makes sure all values are between 0 and 255.
      output.append(max(0, min(255, i/2)))
    if tint == "light":
      output.append(max(0,min(255, i+70)))
  return output


new_colors={"white": [255, 255, 255], "black": [0, 0, 0]}

for color in basic_colors.keys() :
  if color not in ["black", "white","gray"]:   
    new_colors["light "+ color] = add_to_list(basic_colors[color], "light")
    new_colors[color]=basic_colors[color]
    new_colors["dark "+ color] = add_to_list(basic_colors[color], "dark")   
#print(new_colors)
Colors_rgb=list(new_colors.values())
Color_names=list(new_colors.keys())

#for color,value in new_colors.items(): 
#  print (colr.color(f"   {color}", back=value))
#Décommenter pour observer la palette de couleurs de la table

#----------------- Fin creation table de couleurs

def get_colors(link,nb_cluster):
    imgfile = Image.open("image_tests/{link}".format(link=link))
    numarray = np.array(imgfile.getdata(), np.uint8)
    #print(numarray)
    clusters = KMeans(n_clusters = nb_cluster)
    clusters.fit(numarray)
    npbins = np.arange(0, nb_cluster+1)
    histogram = np.histogram(clusters.labels_, bins=npbins)
    labels = np.unique(clusters.labels_)
    barlist = plot.bar(labels, histogram[0])
    for i in range(nb_cluster):
        barlist[i].set_color('#%02x%02x%02x' % (
        math.ceil(clusters.cluster_centers_[i][0]), 
        math.ceil(clusters.cluster_centers_[i][1]),
        math.ceil(clusters.cluster_centers_[i][2])))

    # plot.show()
    a=0
    for i in clusters.cluster_centers_:
        b=0
        for j in i:
            clusters.cluster_centers_[a][b]=int(j)
            b+=1
        a+=1
    
    name_list=[]
    for i in clusters.cluster_centers_:
        tmp_clr=None
        tmp_dist=None
        for stand_col in Colors_rgb:
            if tmp_dist is None or tmp_dist > math.dist(i,stand_col):
                tmp_clr = stand_col
                tmp_dist = math.dist(i,stand_col)
        name_list.append(Color_names[Colors_rgb.index(tmp_clr)])
    return set(name_list)


#------------------------------Déroulement code

img_list = get_n_pics(15)
image_num=0
for img in img_list:
    img_title="{title}.jpg".format(title=img["title"])
    if os.path.isfile("image_tests/{img_title}".format(img_title=img_title))==False:
        download_to_path(img_folder_path, img["jpglink"], img_title)
    else:
        print("ok") 
    img_colors=get_colors(img_title,6)
    img_list[image_num]["colors"]=img_colors

        
def random_sample(n, imglist):
    user_list = rd.sample(imglist,n)
    return user_list

user_choice = random_sample(15,img_list)

