#!/usr/bin/env python3.6

import cv2
import matplotlib
import numpy as np


def analyze_row(img, row_num):
    row = img[row_num]
    groups = []
    i = 0
    while i < len(row):
        current_color = row[i]
        j = i
        current_group = {'indeces': [],
                         'color': current_color
                         }
        while np.array_equal(row[i], row[j]):
            current_group['indeces'].append(j)
            j += 1
            if j == len(row):
                break
        groups.append(current_group)
        i = j
    print(groups)


img = cv2.imread('pics/test1.png')
background = np.array([255, 255, 255])
analyze_row(img, 14)
