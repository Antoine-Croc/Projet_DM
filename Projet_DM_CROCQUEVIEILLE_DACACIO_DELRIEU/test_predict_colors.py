from test_values import IMGS as img_list
from prediction import train_labels_and_trees, is_image_favorite

good_pic_title = "Monkeys_rock_of_Gibraltar"
bad_pic_title = "Notebook_with_open_pages_and_leaves"

def intersect(a, b):
    return [x for x in a if x in b]


def check_for_color(colors, imglist):
    if isinstance(colors, str):
        colors = [colors]
    counter = 0

    for img in imglist:
        if any([color in img["colors"] for color in colors]):
            counter+=1
    print(f"colors is present {counter}/{len(imglist)} times")

#----------------------------- Créer liste en fonction des couleurs
good_pic = [x for x in img_list if x["title"] == good_pic_title][0]
bad_pic = [x for x in img_list if x["title"] == bad_pic_title][0]

good_pic_list = []
for pic in img_list:
    good_colors = intersect(good_pic["colors"], pic["colors"])
    bad_colors = intersect(bad_pic["colors"], pic["colors"])
    if len(bad_colors) < 2 and len(good_colors) > 3:
        pic["liked"] = 1
        good_pic_list.append(pic)

print(f"length of good_pic_list: {len(good_pic_list)}")
print(good_pic_list)

mediocre_pic_list = []
for pic in img_list:
    good_colors = intersect(good_pic["colors"], pic["colors"])
    bad_colors = intersect(bad_pic["colors"], pic["colors"])
    if not(len(bad_colors) < 2 and len(good_colors) > 3) and len(bad_colors) < 3 and len(good_colors) < 3:
        pic["liked"] = 0
        mediocre_pic_list.append(pic)
print(f"length of mediocre_pic_list: {len(mediocre_pic_list)}")
#------------------------


trained = train_labels_and_trees(good_pic_list[:12]+mediocre_pic_list[:15], img_list)
for pic in good_pic_list[13:]:
    is_image_favorite(pic, trained["labels"], trained["trees"])
