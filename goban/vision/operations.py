#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:24:18 2017

@author: taras
"""

import cv2;
import numpy as np;

from goban.math.geometry import sortPointsCW

def bgrToGray(img, dtype = np.uint8):
    return np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), dtype);

def bgrToHsv(img, dtype = None):
    return np.array(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), dtype);

def getChannel(img, channelIndex, dtype = np.uint8):
    channels = cv2.split(img);
    return np.array(channels[channelIndex], dtype);

def rectifyPerspective(img, srcCornerPoints, dstSize, paddingHeight = 0, paddingWidth = 0):
    perspTrans = cv2.getPerspectiveTransform(np.float32(sortPointsCW(srcCornerPoints)), np.float32(sortPointsCW([(paddingWidth,dstSize[0]-paddingHeight),(dstSize[1]-paddingWidth,dstSize[0]-paddingHeight),(paddingWidth,paddingHeight),(dstSize[1]-paddingWidth,paddingHeight)])));
    return cv2.warpPerspective(img, perspTrans, dstSize);
