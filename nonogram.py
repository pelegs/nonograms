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
            if not current_cluster.is_bg:
                self.add_cluster(current_cluster)
            i = j

    def get_data(self):
        if self.num_clusters > 1:
            data = []
            for cluster in self.clusters:
                row = np.zeros(4)
                row[0:3] = cluster.color
                row[3] = cluster.num_elements
                data.append(row)
            return np.array(data)
        return None


class Table:
    rows = []
    cols = []
    max_row_clusters = 0
    max_col_clusters = 0

    def add_row(self, row):
        self.rows.append(row)
        self.max_row_clusters = np.max([row.num_clusters for row in self.rows])


    def add_col(self, col):
        self.cols.append(col)
        self.max_col_clusters = np.max([col.num_clusters for col in self.cols])

    def generate_table(self, img):
        num_rows = img.shape[0] + self.max_col_clusters
        num_cols = img.shape[1] + self.max_row_clusters
        shape = (num_rows, num_cols, 4)
        self.data = (np.ones(shape=shape) * 255).astype(int)

        i = self.max_col_clusters
        for line in self.rows:
            if line.get_data() is not None:
                self.data[i, self.max_row_clusters-line.num_clusters:self.max_row_clusters] = line.get_data()
            i += 1
        j = self.max_row_clusters
        for line in self.cols:
            if line.get_data() is not None:
                self.data[self.max_col_clusters-line.num_clusters:self.max_col_clusters, j] = line.get_data()
            j += 1

    def print(self, frow, lrow):
        for row in self.data:
            print(' '.join(map(str, row)))

    def print_latex(self, background):
        for row in self.data:
            print('&'.join(['\\cellcolor[RGB]{{{}}}{}'.format(','.join(map(str, vals[0:3])), vals[3])
                            if not np.array_equal(vals[0:3], background)
                            else '\\cellcolor[RGB]{{{}}}{}'.format(','.join(map(str, vals[0:3])), '')
                            for vals in row]), '\\\\ \hline')


img = cv2.imread('pics/test2.png', cv2.IMREAD_COLOR)
background = np.array([255, 255, 255])

rows = [line(img, i, type='row', bg=background) for i in range(img.shape[0])]
cols = [line(img, i, type='col', bg=background) for i in range(img.shape[1])]

table = Table()
for row, col in zip(rows, cols):
    table.add_row(row)
    table.add_col(col)
table.generate_table(img)

print('\\begin{tabular}{|' + '|'.join(['p{\\cellsize}' for _ in range(table.data.shape[1])]) + '|}')
table.print_latex(background)
print('\\end{tabular}')
