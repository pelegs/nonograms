#!/usr/bin/env python3.6

import cv2
import matplotlib
import numpy as np


def format_color(color):
    return '\\cellcolor[RGB]{{{}}}'.format(','.join(map(str, color)))

class cluster:
    def __init__(self, color, indeces, num_elements, is_bg=False):
        self.color = color[::-1]
        self.indeces = indeces
        self.num_elements = num_elements
        self.is_bg = is_bg

    def add_index(self, index):
        self.indeces.append(index)
        self.num_elements += 1

    def print_data(self):
        print('{}: {}'.format(self.color, self.num_elements))

    def get_latex(self):
        if self.num_elements > 0 and not self.is_bg:
            return '{}{}'.format(format_color(self.color), self.num_elements)
        else:
            return None


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
            is_bg = np.array_equal(self.data[i], self.bg)
            current_cluster = cluster(color=self.data[i],
                                      indeces=[],
                                      num_elements=0,
                                      is_bg=is_bg)
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

    def print_latex(self, N):
        latex_arr = [cluster.get_latex() for cluster in self.clusters if cluster.get_latex() is not None]
        L = len(latex_arr)
        zeros = N-L
        print('&'.join([' ' for _ in range(zeros)]), end='')
        print('&'.join(latex_arr), '\\\\ \\hline')

    def show(self):
        cv2.imshow('image', self.data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class Table:
    rows = []
    cols = []
    max_row_clusters = 0
    max_col_clusters = 0

    def add_row(self, row):
        self.rows.append(row)
        if row.num_clusters > self.max_row_clusters:
            self.max_row_clusters = row.num_clusters

    def add_col(self, col):
        self.cols.append(col)
        if col.num_clusters > self.max_col_clusters:
            self.max_col_clusters = col.num_clusters

    def generate_table(self, img):
        num_rows = img.shape[0] + self.max_col_clusters
        num_cols = img.shape[1] + self.max_row_clusters
        shape = (num_rows, num_cols, 4)
        self.data = np.zeros(shape=shape)

    def print(self):
        print(self.max_row_clusters, self.max_col_clusters)
        print(self.data.shape)


img = cv2.imread('pics/test1.png', cv2.IMREAD_COLOR)
background = np.array([255, 255, 255])

rows = [line(img, i, type='row', bg=background) for i in range(img.shape[0])]
cols = [line(img, i, type='col', bg=background) for i in range(img.shape[1])]
table = Table()

for row, col in zip(rows, cols):
    table.add_row(row)
    table.add_col(col)
table.generate_table(img)
table.print()
