from test_values import IMGS as img_list
from prediction import train_labels_and_trees, is_image_favorite
from get_img import *

Favorites=[]
NotFavorites=[]

Fav=[]
NFav=[]
allF=Fav+NFav
list_rest=[]

for i in img_list:
	for j in Favorites:
		if i["title"]==j:
			i["liked"]=1
			Fav.append(i)
	for j in NotFavorites:
		if i["title"]==j:
			i["liked"]=0
			NFav.append(i)

for i in img_list:
	if i not in allF:
		list_rest.append(i)

print(allF)


trained = train_labels_and_trees(Fav, allF)
for pic in list_rest:
	is_image_favorite(pic, trained["labels"], trained["trees"])