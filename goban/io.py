#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:40:17 2017

@author: taras
"""

import cv2
import numpy as np
import os
import json
import base64

from goban.board import CellType
from goban.nn import Network

# TODO: Accept additional param to control loaded image format
def loadImage(imageFilename):
    return cv2.imread(imageFilename);

def loadTrainingData(dataFileName, fragmentShape, fragmentFormat = np.uint8):
    if os.path.isfile(dataFileName):
        with open(dataFileName, encoding='utf-8') as infile:
            rawData = json.load(infile);
    else:
        rawData = []
    
    print("There are %d images in the data set." % len(rawData));
    
    data = []
    for rawDatum in rawData:
        image = cv2.imdecode(np.fromstring(base64.b64decode(rawDatum[0]),fragmentFormat), 0);
        if image.shape != fragmentShape:
            raise ValueError("Invalid image shape %s: expected %s" % (str(image.shape), str(fragmentShape)));
        cellType = CellType(rawDatum[1])
        data.append((image, cellType));
    
    return data

def saveTrainingData(data, dataFileName, fragmentShape = None, encFormat = '.jpg'):
    # Encode and save data
    encData = [];
    for datum in data:
        if (fragmentShape != None) and (datum[0].shape != fragmentShape):
            raise ValueError("All images in the saved set must have the same shape; epxected: %s, got %s" % (str(fragmentShape), str(datum[0].shape)));
        if fragmentShape == None:
            fragmentShape = datum[0].shape
        encImage = base64.b64encode(cv2.imencode(encFormat, datum[0])[1].tostring()).decode('ascii');
        encCellType = datum[1].value;
        encData.append((encImage, encCellType));
    
    with open(dataFileName, 'w') as outfile:
        json.dump(encData, outfile);

def loadNeuralNetwork(networkFileName):
    if not os.path.isfile(networkFileName):
        raise IOError("Neural network file %s not found!" % networkFileName);
    with open(networkFileName, encoding='utf-8') as infile:
        networkData = json.load(infile);
    neuralNet = Network(networkData['sizes']);
    neuralNet.biases = [np.array(bi) for bi in networkData['biases']];
    neuralNet.weights = [np.array(wi) for wi in networkData['weights']];
    neuralNet.num_layers = networkData['num_layers'];
    return neuralNet;

def saveNeuralNetwork(network, networkFileName):
    # Save network
    with open(networkFileName, 'w') as outfile:
        json.dump( \
            {"biases":[bi.tolist() for bi in network.biases],
            "num_layers":network.num_layers,
            "sizes":network.sizes,
            "weights":[wi.tolist() for wi in network.weights]},
            outfile
        );
