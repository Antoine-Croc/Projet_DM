from sklearn import tree
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import graphviz
import pydotplus
from IPython.display import Image, display
from colors import full_colors, print_colors


OTHER_KEYS = ["height", "width", "orientation"]
EXPLODED_KEYS = ["colors", "keywords"]

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

def train_labels_and_trees(user_choice, all_pictures):
    choice_df = pd.DataFrame(user_choice)
    choice_df = drop_all_except(
        choice_df,
        ["colors", "height", "width", "orientation", "keywords", "liked"],
    )
    results = choice_df["liked"]

    labels = {}
    exploded_df = {}
    for key in ["colors", "height", "width", "orientation", "keywords"]:
        labels[key] = LabelEncoder()
        labels[key].fit(get_unique_values(key, all_pictures))
        if key in EXPLODED_KEYS:
            exploded_df[key] = drop_all_except(choice_df, [key, "liked"]).explode(key)
            exploded_df[key][key] = labels[key].transform(exploded_df[key][key])
        else:
            others_df = drop_all_except(choice_df, [*OTHER_KEYS, "liked"])
            others_df[key] = labels[key].transform(others_df[key])


    trees = {}
    for key in EXPLODED_KEYS:
        trees[key] = tree.DecisionTreeClassifier()
        trees[key].fit(
            exploded_df[key][key].to_frame(), exploded_df[key]["liked"].to_frame()
        )

    trees["others"] = tree.DecisionTreeClassifier()
    trees["others"].fit(others_df[OTHER_KEYS], others_df["liked"].to_frame())
    return {"labels": labels, "trees":trees}


def is_image_favorite(img, labels, trees):
    img_df = pd.DataFrame([img])
    other_df = drop_all_except(img_df, OTHER_KEYS)
    for key in OTHER_KEYS:
        other_df[key] = labels[key].transform(other_df[key])
    other_prediction = trees["others"].predict(other_df)

    exploded_preds = {}
    for key in EXPLODED_KEYS:
        exploded_df = drop_all_except(img_df, [key]).explode(key)
        exploded_df = pd.DataFrame(labels[key].transform(exploded_df))
        exploded_preds[key] = trees[key].predict(exploded_df)

    print("others: ", other_prediction)
    for key, pred in exploded_preds.items():
        print(f"{key}: {pred}")

    color_prediction = list(exploded_preds["colors"]).count(0) < 2
    keywords_prediction = list(exploded_preds["keywords"]).count(0) < len(exploded_preds["keywords"])//3
    other_prediction = bool(other_prediction[0])
    return color_prediction and keywords_prediction and other_prediction