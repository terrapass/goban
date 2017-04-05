#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:23:30 2017

@author: taras
"""

import cv2;
import numpy as np;
from enum import Enum;

from goban.board import CellType

class ConfidenceMeasure(Enum):
    MAX_OUTPUT = 0;
    MAX_OUTPUT_MINUS_OTHERS = 1;

def asInputVector(image):
    return (np.float32(image)/255).reshape((image.size,1));

def asOutputVector(cellType):
    result = np.zeros((3,1), np.float32);
    result[cellType.value] = 1.0;
    return result;

def interpret(networkOutputVector, confidenceThreshold = 0.0, confidenceMeasure = ConfidenceMeasure.MAX_OUTPUT):
    index = None;
    maxValue = 0;
    for i in range(0,len(networkOutputVector)):
        if networkOutputVector[i] > maxValue:
            index = i;
            maxValue = networkOutputVector[i];
    confidence = maxValue if confidenceMeasure == ConfidenceMeasure.MAX_OUTPUT \
        else maxValue - sum([networkOutputVector[i] if i != index else 0 for i in range(0, len(networkOutputVector))]);
    if confidence < confidenceThreshold:
        raise RuntimeError("NN is not confident enough (confidence: %f, required: %f)" % (maxValue, confidenceThreshold));
    return CellType(index), confidence;

def getConfidence(networkOutputVector, confidenceMeasure = ConfidenceMeasure.MAX_OUTPUT):
    index = None;
    maxValue = 0;
    for i in range(0,len(networkOutputVector)):
        if networkOutputVector[i] > maxValue:
            index = i;
            maxValue = networkOutputVector[i];
    confidence = maxValue if confidenceMeasure == ConfidenceMeasure.MAX_OUTPUT \
        else maxValue - sum([networkOutputVector[i] if i != index else 0 for i in range(0, len(networkOutputVector))]);
    return confidence

def enrichWithRotations(data):
    rotatedData = []
    for datum in data:
        rotated_img = datum[0].copy();
        for i in range(0,3):
            rotated_img = cv2.flip(cv2.transpose(rotated_img), flipCode=0);
            rotatedData.append((rotated_img.copy(), datum[1]));
    data += rotatedData;
#import matplotlib.pyplot as plt
def enrichWithFlips(data):
    flippedData = []
    for datum in data:
        for i in range(0,2):
            flipped_img = cv2.flip(datum[0].copy(), flipCode=i);
            flippedData.append((flipped_img.copy(), datum[1]));
#    for flippedDatum in flippedData:
#        plt.imshow(flippedDatum[0], 'gray');
#        plt.show();
#        input();
    data += flippedData;
