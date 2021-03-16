import requests
from bs4 import BeautifulSoup as bs


img_folder_path = "/home/antoine/Documents/Images_Projet/image_tests" # replace with absolute path of image folder

url = "https://www.4freephotos.com/"
# print(soup.prettify()) to see the html code


def get_page(page_num):
    page_url = "https://www.4freephotos.com/photos.php?&page={page_num}&order=latest"
    req = requests.get(page_url.format(page_num=page_num))
    soup = bs(req.text, 'html.parser')
    return soup


def get_n_pics(n):
    page_num = 0
    img_list = []
    while len(img_list) < n:
        page_num += 1
        soup = get_page(page_num)
        for img in soup.find_all("img"):
          if img.get("height") and img.get("width"):
            # img_list.append(img) <-- list of tags
            img_list.append(
                jsonify(img) # list of jsonified_tags
            )
    img_list = img_list[:n]
    return img_list

def jsonify(tag):
    jsonified_tag = {}
    jsonified_tag["link"] = "https://www.4freephotos.com/" + tag["src"] # To get correct full link to pictures
    jsonified_tag["height"] = tag["height"]
    jsonified_tag["width"] = tag["width"]
    jsonified_tag["attributes"] = tag["alt"]
    return jsonified_tag

def download_to_path(path, url, name):
    r = requests.get(url)
    with open(path + "/" + name, "wb") as writer: # replace \\ with /
        writer.write(r.content)

img_list = get_n_pics(10)
for count, img in enumerate(img_list):
    download_to_path(img_folder_path, img["link"], "pic_number_{count}.jpg".format(count=count))
