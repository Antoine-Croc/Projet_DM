from PIL import Image
import numpy
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans
imgfile = Image.open("image_tests/pic_number_0.jpg")
numarray = numpy.array(imgfile.getdata(), numpy.uint8)
# print("entrez le nombre de cluster:nombre entier")
# nb_cluster=int(input())
nb_cluster=3
clusters = KMeans(n_clusters = nb_cluster)
clusters.fit(numarray)
npbins = numpy.arange(0, nb_cluster+1)
histogram = numpy.histogram(clusters.labels_, bins=npbins)
labels = numpy.unique(clusters.labels_)
barlist = plot.bar(labels, histogram[0])
for i in range(nb_cluster):
    barlist[i].set_color('#%02x%02x%02x' % (
    math.ceil(clusters.cluster_centers_[i][0]), 
        math.ceil(clusters.cluster_centers_[i][1]),
    math.ceil(clusters.cluster_centers_[i][2])))
plot.show()
