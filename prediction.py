from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import graphviz
import pydotplus
from IPython.display import Image, display

data = [
    ['green', 'nature', 'thumbnail', 'landscape'], 
    ['blue', 'architecture', 'medium', 'portrait'],
    ['blue', 'people', 'medium', 'landscape'],
    ['yellow', 'nature', 'medium', 'portrait'],
    ['green', 'nature', 'thumbnail', 'landscape'],
    ['blue', 'people', 'medium', 'landscape'],
    ['blue', 'nature', 'thumbnail', 'portrait'],
    ['yellow', 'architecture', 'thumbnail', 'landscape'],
    ['blue', 'people', 'medium', 'portrait'],
    ['yellow', 'nature', 'medium', 'landscape'],
    ['yellow', 'people', 'thumbnail', 'portrait'],
    ['blue', 'people', 'medium', 'landscape'],
    ['red', 'architecture', 'thumbnail','landscape']]
result = [
    'Favorite',
    'NotFavorite',
	'Favorite',
    'Favorite',
    'Favorite',
    'Favorite',
    'Favorite',
    'NotFavorite',
    'NotFavorite',
    'Favorite',
    'Favorite',
    'NotFavorite',
    'NotFavorite'
    ]

#creating dataframes
dataframe = pd.DataFrame(data, columns=['colors', 'tag', 'size', 'mode'])
resultframe = pd.DataFrame(result, columns=['favorite'])

#generating numerical labels
le1 = LabelEncoder()
dataframe['colors'] = le1.fit_transform(dataframe['colors'])

le2 = LabelEncoder()
dataframe['tag'] = le2.fit_transform(dataframe['tag'])

le3 = LabelEncoder()
dataframe['size'] = le3.fit_transform(dataframe['size'])

le4 = LabelEncoder()
dataframe['mode'] = le4.fit_transform(dataframe['mode'])

le5 = LabelEncoder()
resultframe['favorite'] = le5.fit_transform(resultframe['favorite'])
   
#Use of decision tree classifiers
dtc = tree.DecisionTreeClassifier()
dtc = dtc.fit(dataframe, resultframe)

    #prediction
prediction = dtc.predict([
    [le1.transform(['red'])[0], le2.transform(['nature'])[0],
    le3.transform(['thumbnail'])[0], le4.transform(['portrait'])[0]]])
print(le5.inverse_transform(prediction))
print(dtc.feature_importances_)
    
dot_data = tree.export_graphviz(dtc, out_file=None,
    feature_names=dataframe.columns,
    filled=True, rounded=True, 
    class_names =
    le5.inverse_transform(
    resultframe.favorite.unique())
    ) 
graph = graphviz.Source(dot_data)     
pydot_graph = pydotplus.graph_from_dot_data(dot_data)
img = Image(pydot_graph.create_png())
display(img)

