from PIL import Image
import cv2
import numpy 
import numpy as np
from numpy import uint8
import matplotlib.pyplot as plt
import csv
import time
import os


ndvi_values = [-1.00, -0.95, 
               -0.90, -0.85, 
               -0.80, -0.75, 
               -0.70, -0.65, 
               -0.60, -0.55, 
               -0.50, -0.45, 
               -0.40, -0.35, 
               -0.30, -0.25, 
               -0.20, -0.15, 
               -0.10, -0.05, 
               +0.00, 
               +0.05, +0.10, 
               +0.15, +0.20, 
               +0.25, +0.30, 
               +0.35, +0.40, 
               +0.45, +0.50, 
               +0.55, +0.60, 
               +0.65, +0.70, 
               +0.75, +0.80, 
               +0.85, +0.90, 
               +0.95, +1.00]

ndvi_colors = [ [  5,  5,  5], [ 14, 14, 14], 
                [ 29, 29, 29], [ 43, 43, 43], 
                [ 60, 60, 60], [ 75, 75, 75], 
                [ 90, 90, 90], [104,104,104], 
                [121,121,121], [136,136,136], 
                [150,150,150], [166,166,166], 
                [180,180,180], [196,196,196], 
                [222, 76, 75], [231, 90, 72], 
                [241,104, 68], [246,122, 73], 
                [248,140, 82], [251,158, 90], 
                [253,178,100],
                [253,193,112], [254,208,126],
                [254,223,138], [254,232,152],
                [255,241,168], [255,250,185],
                [251,253,185], [242,250,171],
                [236,248,161], [224,243,153],
                [209,236,156], [190,229,160],
                [173,221,164], [152,214,164],
                [131,205,165], [112,197,165],
                [ 94,185,169], [ 77,167,176],
                [ 62,149,183], [ 52,134, 87] ]

frequency = [0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0,
             0, 0]

weighted_mean = 0
major_element = 0


def threeD_colorspace_euclideanDistance(c1_R, c1_G, c1_B, c2_R, c2_G, c2_B):
    return (c1_R-c2_R)**2 + (c1_G-c2_G)**2 + (c1_B-c2_B)**2

def main():
    header = ['Name', 'Major NDVI', 'Major element', 'Mean NDVI']
    with open('image_data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for idx in range(0,537):
            image_string = (str(idx) if idx>=100 else ('0'+str(idx) if idx>=10 else '00'+str(idx))) + "-prepared.jpg"
            
            if os.path.isfile(image_string)==True:
                print('found' + str(idx))
                # initialise variables
                weighted_mean, major_element = [0, 0]
                for k in range(0,41):
                    frequency[k] = 0

                # analyse image
                im_ndvi= Image.open(image_string)
                pix = im_ndvi.load()
                height, width = im_ndvi.size
                for x in range(0,height):
                    for y in range(0,width): 
                        r,g,b = pix[x,y] # RGBA tuple for .png; RGB tuple for .jpg
                        # check if cell is valid (!= white)
                        if r!=255 or g!=255 or b!=255:
                            best_poz = 0
                            if r==g and g==b:
                                left, right = [0,14]
                            else:
                                left, right = [14,41]
                            # find best fit
                            for k in range(left,right):
                                candidate_R = ndvi_colors[k][0]
                                candidate_G = ndvi_colors[k][1]
                                candidate_B = ndvi_colors[k][2]
                                best_R = ndvi_colors[best_poz][0]
                                best_G = ndvi_colors[best_poz][1]
                                best_B = ndvi_colors[best_poz][2]
                                if threeD_colorspace_euclideanDistance(r,g,b, candidate_R, candidate_G, candidate_B) < threeD_colorspace_euclideanDistance(r,g,b, best_R, best_G, best_B):
                                    best_poz = k
                            # update in freq[] vector
                            frequency[best_poz] += 1
                            # update mean
                            weighted_mean += ndvi_values[best_poz]
                
                # find which value has highest frequency
                max_idx = 0
                for k in range(0,41):
                    if frequency[k] > frequency[max_idx]:
                        max_idx = k
                major_element = ndvi_values[max_idx]

                # calculate weighted mean
                cnt = 0
                for k in range(0,41):
                    cnt += frequency[k]
                weighted_mean /= cnt
                
                writer.writerow([image_string, major_element, str(ndvi_colors[max_idx][0])+','+str(ndvi_colors[max_idx][1])+','+str(ndvi_colors[max_idx][2]), weighted_mean])


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))