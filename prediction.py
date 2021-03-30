from sklearn import tree
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import graphviz
import pydotplus
from IPython.display import Image, display
from get_img import user_choice, img_list
from colors import full_colors, print_colors


def get_unique_values(key, imglist):
    payload = set()
    for img in imglist:
        if isinstance(img[key], list) or isinstance(img[key], set):
            for elt in img[key]:
                payload.add(elt)
        else:
            payload.add(img[key])
    return list(payload)


def drop_all_except(df, cols):
    payload = df
    for col in df.columns:
        if col not in cols:
            payload = payload.drop(col, axis=1)
    return payload


choice_df = pd.DataFrame(user_choice)
choice_df = drop_all_except(
    choice_df,
    ["colors", "height", "width", "orientation", "keywords", "liked"],
)
results = choice_df["liked"]

labels = {}
exploded_df = {}
other_keys = ["height", "width", "orientation"]
exploded_keys = ["colors", "keywords"]


for key in ["colors", "height", "width", "orientation", "keywords"]:
    labels[key] = LabelEncoder()
    print(key)
    print(get_unique_values(key, img_list))
    labels[key].fit(get_unique_values(key, img_list))
    if key in exploded_keys:
        exploded_df[key] = drop_all_except(choice_df, [key, "liked"]).explode(key)
        exploded_df[key][key] = labels[key].transform(exploded_df[key][key])
    else:
        others_df = drop_all_except(choice_df, [*other_keys, "liked"])
        choice_df[key] = labels[key].transform(others_df[key])


trees = {}
for key in exploded_keys:
    trees[key] = tree.DecisionTreeClassifier()
    trees[key].fit(exploded_df[key][key], exploded_df[key]["liked"])

trees["others"] = tree.DecisionTreeClassifier()
trees["others"].fit(others_df[other_keys], others_df["liked"])


# def is_image_favorite(img, labels=labels, trees=trees):
#

exit()
# creating dataframes
dataframe = pd.DataFrame(data, columns=["colors", "tag", "size", "mode"])
resultframe = pd.DataFrame(result, columns=["favorite"])

# generating numerical labels
color_label = LabelEncoder()
color_label.fit(color_names)
dataframe["colors"] = le1.fit_transform(dataframe["colors"])

le2 = LabelEncoder()
dataframe["tag"] = le2.fit_transform(dataframe["tag"])

le3 = LabelEncoder()
dataframe["size"] = le3.fit_transform(dataframe["size"])

le4 = LabelEncoder()
dataframe["mode"] = le4.fit_transform(dataframe["mode"])

le5 = LabelEncoder()
resultframe["favorite"] = le5.fit_transform(resultframe["favorite"])

# Use of decision tree classifiers
dtc = tree.DecisionTreeClassifier()
dtc = dtc.fit(dataframe, resultframe)

# prediction
prediction = dtc.predict(
    [
        [
            le1.transform(["red"])[0],
            le2.transform(["nature"])[0],
            le3.transform(["thumbnail"])[0],
            le4.transform(["portrait"])[0],
        ]
    ]
)
print(le5.inverse_transform(prediction))
print(dtc.feature_importances_)
