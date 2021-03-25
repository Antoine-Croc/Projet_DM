import colr

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


def limit_list(rgb_list, tint):
  output = []
  for i in rgb_list:
    if tint == "dark":
    # Makes sure all values are between 0 and 255.
      output.append(max(0, min(255, i/2)))
    if tint == "light":
      output.append(max(0,min(255, i+70)))
  return output


new_colors={"white": [255, 255, 255], "black": [0, 0, 0]}

for color in colors.keys() :
  if color not in ["black", "white"]:    
    new_colors["light "+ color] = limit_list(colors[color], "light")
    new_colors[color]=colors[color]
    new_colors["dark "+ color] = limit_list(colors[color], "dark")    

for color,value in new_colors.items(): 
  print (colr.color(f"   {color}", back=value))