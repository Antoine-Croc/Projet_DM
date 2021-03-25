from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plot
import colr
from sklearn.cluster import KMeans

imgfile = Image.open("image_tests/Exit_signs_in_airport.jpg")
numarray = np.array(imgfile.getdata(), np.uint8)

#------------------Creation de la table de couleurs

# colors = {
#   "white": [255, 255, 255],
#   "black": [0, 0, 0],
#   "red": [255, 0, 0],
#   "green": [0, 255, 0],
#   "blue": [0, 0, 255],
#   "yellow": [255,255,0],
#   "cyan": [0,255,255],
#   "magenta": [255,0,255],
#   "gray": [128,128,128],
#   "orange": [255, 128, 0],
#   "purple": [128, 0, 255],
#   "pink": [255, 0, 128],
#   "brown": [165,42,42],
# }


# def add_to_list(rgb_list, tint):
#   output = []
#   for i in rgb_list:
#     if tint == "dark":
#     # Makes sure all values are between 0 and 255.
#       output.append(max(0, min(255, i/2)))
#     if tint == "light":
#       output.append(max(0,min(255, i+70)))
#   return output


# new_colors={"white": [255, 255, 255], "black": [0, 0, 0]}

# for color in colors.keys() :
#   if color not in ["black", "white"]:    
#     new_colors["light "+ color] = add_to_list(colors[color], "light")
#     new_colors[color]=colors[color]
#     new_colors["dark "+ color] = add_to_list(colors[color], "dark")    
# print(new_colors)

#for color,value in new_colors.items(): 
#  print (colr.color(f"   {color}", back=value))
#Décommenter pour observer la palette de couleurs de la table

#----------------- Fin creation table de couleurs

Colors_rgb=[
[255, 255, 255], [0, 0, 0], 
[255, 70, 70], [255, 0, 0], [127.5, 0, 0], 
[70, 255, 70], [0, 255, 0], [0, 127.5, 0], 
[70, 70, 255], [0, 0, 255], [0, 0, 127.5], 
[255, 255, 70], [255, 255, 0], [127.5, 127.5, 0], 
[70, 255, 255], [0, 255, 255], [0, 127.5, 127.5], 
[255, 70, 255], [255, 0, 255], [127.5, 0, 127.5],
[198, 198, 198], [128, 128, 128], [64.0, 64.0, 64.0],
[255, 198, 70], [255, 128, 0], [127.5, 64.0, 0], 
[198, 70, 255], [128, 0, 255], [64.0, 0, 127.5], 
[255, 70, 198],[255, 0, 128], [127.5, 0, 64.0],
[235, 112, 112],[165, 42, 42], [82.5, 21.0, 21.0]
]
Colors_names=["white","black",
'light red',"red","dark red",
"light green","green","dark green",
"light blue","blue","dark blue",
"light yellow","yellow","dark yellow",
"light cyan","cyan","dark cyan",
"light magenta","magenta","dark magenta",
"light gray","gray","dark gray",
"light orange","orange","dark orange",
"light purple","purple","dark purple",
"light pink","pink","dark pink",
"light brown","brown","dark brown"]

# print("entrez le nombre de cluster:nombre entier")
# nb_cluster=int(input())

nb_cluster=2

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


 

def closest(colors,color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance,index_of_smallest

for i in clusters.cluster_centers_:
    closest_color,color_index = closest(Colors_rgb,i)
    colorname = Colors_names[color_index[0][0]]
    print (closest_color)
    print (Colors_names[color_index[0][0]])
    #print (colr.color(colorname,closest_color[0][0]))




