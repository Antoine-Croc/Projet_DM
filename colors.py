import colr

base_colors = {
    "white": [255, 255, 255],
    "black": [0, 0, 0],
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "yellow": [255, 255, 0],
    "cyan": [0, 255, 255],
    "magenta": [255, 0, 255],
    "gray": [128, 128, 128],
    "orange": [255, 128, 0],
    "purple": [128, 0, 255],
    "pink": [255, 0, 128],
    "brown": [165, 42, 42],
}


def limit_list(rgb_list, tint):
    output = []
    for i in rgb_list:
        if tint == "dark":
            # Makes sure all values are between 0 and 255.
            output.append(max(0, min(255, i / 2)))
        if tint == "light":
            output.append(max(0, min(255, i + 70)))
    return output


full_colors = {"white": [255, 255, 255], "black": [0, 0, 0]}

for color in base_colors.keys():
    if color not in ["black", "white"]:
        full_colors["light " + color] = limit_list(base_colors[color], "light")
        full_colors[color] = base_colors[color]
        full_colors["dark " + color] = limit_list(base_colors[color], "dark")


def print_colors(palette):
    black = full_colors["black"]
    for color, value in palette.items():
        print(
            colr.color(
                f"   {color}",
                back=value,
                fore=black if value != black else full_colors["white"],
            )
        )
