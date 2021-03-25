#closest color test
import numpy as np
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
color_names=["white","black",
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


to_test=[
    [221.5081787, 194.2691022, 224.55181328],
    [144.41227747, 165.65952098, 105.557145]
    ]  
a=0
for i in to_test:
    b=0
    for j in i:
        to_test[a][b]=int(j)
        b+=1
    a+=1
print(to_test)
        




def closest(colors_table,color):
    colors_table = np.array(colors_table)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors_table-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors_table[index_of_smallest]
    return smallest_distance 

#for i in color:
#    closest_color = closest(list_of_colors,i)
#print(closest_color )