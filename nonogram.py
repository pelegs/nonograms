#!/usr/bin/env python3.6

import cv2
import matplotlib
import numpy as np


class cluster:
    def __init__(self, color, indeces, num_elements):
        self.color = color
        self.indeces = indeces
        self.num_elements = num_elements

    def add_index(self, index):
        self.indeces.append(index)
        self.num_elements += 1

    def print_data(self):
        print('{}: {}'.format(self.color, self.num_elements))

    def print_latex(self):
        if self.num_elements == 0:
            N = ''
        else:
            N = self.num_elements
        print('\\Z{{ {} }}{}'.format(self.color, N))


class line:
    def __init__(self, img, index, type, bg):
        if type == 'row':
            self.data = img[index,:]
        elif type == 'col':
            self.data = img[:,index]
        else:
            raise ValueError('Type {} unknown'.format(type))
        self.bg = bg

        self.clusters = []
        self.length = self.data.shape[0]
        self.num_clusters = 0

        self.analyze()

    def add_cluster(self, cluster):
        self.clusters.append(cluster)
        self.num_clusters += 1

    def analyze(self):
        i = 0
        while i < self.data.shape[0]:
            j = i
            current_cluster = cluster(color=self.data[i],
                                      indeces=[],
                                      num_elements=0)
            while np.array_equal(self.data[i], self.data[j]):
                current_cluster.add_index(j)
                j += 1
                if j == self.length:
                    break
            self.add_cluster(current_cluster)
            i = j

    def print_data(self, withbg=False):
        for cluster in self.clusters:
            if withbg:
                cluster.print_data()
            else:
                if not np.array_equal(self.bg, cluster.color):
                    cluster.print_data()

    def show(self):
        cv2.imshow('image', self.data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


img = cv2.imread('pics/test1.png', cv2.IMREAD_COLOR)
background = np.array([255, 255, 255])
