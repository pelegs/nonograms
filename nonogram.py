#!/usr/bin/env python3.6

import cv2
import matplotlib
import numpy as np


def analyze(img, index, type='rows'):
    if type == 'rows':
        row = img[index,:]
    else:
        row = img[:,index]
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
        if not (np.array_equal(current_color, background)):
            groups.append(current_group)
        i = j
    return groups

img = cv2.imread('pics/test1.png')
background = np.array([255, 255, 255])
