from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plot
import colr
from sklearn.cluster import KMeans



#------------------Creation de la table de couleurs

colors = {
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
		if tint == "dark": #Makes sure all values are between 0 and 255.
			output.append(max(0, min(255, i/2)))
		if tint == "light":
			output.append(max(0,min(255, i+70)))
	return output


new_colors={"white": [255, 255, 255], "black": [0, 0, 0]}

for color in colors.keys() :
	if color not in ["black", "white"]:    
		new_colors["light "+ color] = add_to_list(colors[color], "light")
		new_colors[color]=colors[color]
		new_colors["dark "+ color] = add_to_list(colors[color], "dark")    
print(new_colors)
Colors_rgb=list(new_colors.values())
Color_names=list(new_colors.keys())


#for color,value in new_colors.items(): 
#  print (colr.color(f"   {color}", back=value))
#Décommenter pour observer la palette de couleurs de la table

#----------------- Fin creation table de couleurs

# print("entrez le nombre de cluster:nombre entier")
# nb_cluster=int(input())


def get_colors(link,nb_cluster):
	imgfile = Image.open("image_tests/{link}.jpg".format(link=link))
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

	clr_list=[]
	name_list=[]
	for i in clusters.cluster_centers_:
		closest_color,color_index = closest(Colors_rgb,i)
		colorname = Color_names[color_index[0][0]]
		print (closest_color)
		#print (Color_names[color_index[0][0]])
		#print (colr.color(colorname,closest_color[0][0]))
	return clr_list,name_list



def closest(colors,color):
	colors = np.array(colors)
	color = np.array(color)
	distances = np.sqrt(np.sum((colors-color)**2,axis=1))
	index_of_smallest = np.where(distances==np.amin(distances))
	smallest_distance = colors[index_of_smallest]
	return smallest_distance,index_of_smallest