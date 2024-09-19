# This script will convert an image file (.jpg, .png, etc) to a RPG Maker MV map file (.json),
# the output json file will be stored in the same directory, with same name of the input image file.
# It takes following color mapping:
#
# 0000FF (deep blue): ocean
# 00FFFF (light blue): river
# 00FF00 (light green): grass
# FFFF00 (yellow): land
# FFFFFF (white): ice
# FF0000 (red): mountain
# 006633 (deep green): trees
#
# Anything other than this will take the closest color mapping.
# It is recommended to resize your image to 256 x 256 or less, and process your image to include only
# these colors before convert, otherwise the result may not be desirable.
#
# After conversion, copy the json file to your game project\data directory, and change the name to
# the map you want to replace, such as Map001.json, then reload your game.

from PIL import Image
import numpy as np
from tkinter import filedialog
import os
from pathlib import Path

#import random
#import tkinter as tk
#root = tk.Tk()
#root.withdraw()

file_path = filedialog.askopenfilename()

if file_path == "":
    exit()

file_dir = os.path.dirname(file_path)
out_file_name = file_dir + "/" + Path(file_path).stem + ".json"
im = Image.open(file_path)

if im.width > 256 or im.height > 256:
    if im.width > im.height:
            r = 256 / im.width
            print(f"resized A, r={r}, h={int(im.height * r)}")
            im = im.resize((256, int(im.height * r)))
    else:
            r = 256 / im.height
            print(f"resized B, r={r}, h={int(im.width * r)}")
            im = im.resize((int(im.width * r), 256))

inpix = im.load()
width = im.width
height = im.height

outpix = [[[0 for x in range(6)] for x in range(width)] for x in range(height)]

ocean_rgb = [0, 0, 255]
river_rgb = [0, 255, 255]
grass_rgb = [0, 255, 0]
land_rgb = [255, 255, 0]
ice_rgb = [255, 255, 255]
mountain_rgb = [255, 0, 0]
tree_rgb = [0, 102, 51]
feature = np.zeros (7)
#rgbvalue = ""
#debugf = open(debug_file_name, "wb")

for h in range(height):
    for w in range(width):
        L0 = 0
        L1 = 0
        L2 = 0
        L3 = 0
        L4 = 0
        L5 = 0

        #print (f"w={w},h={h},p={inpix[w, h]},s={len(inpix[w, h])}")

        if len(inpix[w, h]) == 4 and inpix[w, h][3] == 0:
            # Transparent pixel

            pass
        else:
            # The calculation is to find the deviation of the source pixel to the feature pixel
            # After summing up, the feature with minimum deviation is selected

            feature[0] = abs(inpix[w, h][0] - ocean_rgb[0]) + abs(inpix[w, h][1] - ocean_rgb[1]) + abs(inpix[w, h][2] - ocean_rgb[2])
            feature[1] = abs(inpix[w, h][0] - river_rgb[0]) + abs(inpix[w, h][1] - river_rgb[1]) + abs(inpix[w, h][2] - river_rgb[2])
            feature[2] = abs(inpix[w, h][0] - grass_rgb[0]) + abs(inpix[w, h][1] - grass_rgb[1]) + abs(inpix[w, h][2] - grass_rgb[2])
            feature[3] = abs(inpix[w, h][0] - land_rgb[0]) + abs(inpix[w, h][1] - land_rgb[1]) + abs(inpix[w, h][2] - land_rgb[2])
            feature[4] = abs(inpix[w, h][0] - ice_rgb[0]) + abs(inpix[w, h][1] - ice_rgb[1]) + abs(inpix[w, h][2] - ice_rgb[2])
            feature[5] = abs(inpix[w, h][0] - mountain_rgb[0]) + abs(inpix[w, h][1] - mountain_rgb[1]) + abs(inpix[w, h][2] - mountain_rgb[2])
            feature[6] = abs(inpix[w, h][0] - tree_rgb[0]) + abs(inpix[w, h][1] - tree_rgb[1]) + abs(inpix[w, h][2] - tree_rgb[2])
            fidx = np.argmin(feature)

            if fidx == 0:
                L0 = 2048
                L1 = 2096
            elif fidx == 1:
                L0 = 2048
            elif fidx == 2:
                L0 = 2912
                L1 = 2960
            elif fidx == 3:
                L0 = 3200
            elif fidx == 4:
                L0 = 3968
            elif fidx == 5:
                L0 = 3584
                L1 = 3536
            elif fidx == 6:
                L0 = 3008

            outpix[h][w][0] = L0
            outpix[h][w][1] = L1
            outpix[h][w][2] = L2
            outpix[h][w][3] = L3
            outpix[h][w][4] = L4
            outpix[h][w][5] = L5

f = open(out_file_name, "wb")
f.write(bytes('{\n', encoding='utf-8'))
f.write(bytes('"autoplayBgm":false,"autoplayBgs":false,"battleback1Name":"","battleback2Name":"",', encoding='utf-8'))
f.write(bytes('"bgm":{"name":"","pan":0,"pitch":100,"volume":90},', encoding='utf-8'))
f.write(bytes('"bgs":{"name":"","pan":0,"pitch":100,"volume":90},',  encoding='utf-8'))
f.write(bytes('"disableDashing":false,"displayName":"","encounterList":[],',  encoding='utf-8'))
f.write(bytes(f'"encounterStep":30,"height":{height},"note":"","parallaxLoopX":false,', encoding='utf-8'))
f.write(bytes('"parallaxLoopY":false,"parallaxName":"",',  encoding='utf-8'))
f.write(bytes('"parallaxShow":true,"parallaxSx":0,"parallaxSy":0,"scrollType":0,', encoding='utf-8'))
f.write(bytes('"specifyBattleback":false,',  encoding='utf-8'))
f.write(bytes(f'"tilesetId":1,"width":{width},\n',  encoding='utf-8'))
f.write(bytes('"data":[',  encoding='utf-8'))

comma = 0
for l in range(6):
    for h in range(height):
        for w in range(width):
            if comma > 0:
                f.write(bytes(f",", encoding='utf-8'))
            comma+=1
            f.write(bytes(f"{outpix[h][w][l]}", encoding='utf-8'))

f.write(bytes('],\r', encoding='utf-8'))
f.write(bytes('"events":[\r', encoding='utf-8'))
f.write(bytes('null,\r', encoding='utf-8'))
f.write(bytes('null\r', encoding='utf-8'))
f.write(bytes(']\r', encoding='utf-8'))
f.write(bytes('}', encoding='utf-8'))
f.close()

print(f"Exported to {out_file_name}")
