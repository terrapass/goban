#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:38:52 2017

@author: taras
"""

import cv2;

class Segmentation:
    def __init__(self, img, cols, rows, segmentSize = None):
        self.img = img;
        self.cols = cols;
        self.rows = rows;
        self.segmentSize = segmentSize;
        self.widthStep = img.shape[1] // self.cols;
        self.heightStep = img.shape[0] // self.rows;
        
    def __getitem__(self, key):
        if (type(key) == int):
            i = key // self.rows;
            j = key % self.rows;
        elif (type(key) == tuple):
            i = key[0];
            j = key[1];
        if (i < 0) or (i >= self.rows) or (j < 0) or (j >= self.cols):
            raise IndexError;
        fragment_y = i*self.heightStep;
        fragment_x = j*self.widthStep;
        fragment = self.img[fragment_y:(fragment_y + self.heightStep), fragment_x:(fragment_x + self.widthStep)].copy();
        return fragment if self.segmentSize == None else cv2.resize(fragment, self.segmentSize);
