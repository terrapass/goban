#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 22:05:00 2017

@author: taras
"""
import random
import os

from goban.io import loadTrainingData, saveNeuralNetwork
from goban.nnutils import asInputVector, asOutputVector, enrichWithFlips, enrichWithRotations
from goban.nn import Network
from goban.ui.console import yesno

import config

data = loadTrainingData(config.DATA_FILENAME, config.FRAGMENT_SIZE);

if config.TRAINING_ADD_ROTATIONS:
    enrichWithRotations(data);
if config.TRAINING_ADD_FLIPS:
    enrichWithFlips(data);

if len(data) <= config.VALIDATION_SET_SIZE:
    print("Not enough data points for validation set size %d!" % config.VALIDATION_SET_SIZE);
    exit(1);

print("Training set size: %d\nValidation set size: %d" % (len(data)-config.VALIDATION_SET_SIZE, config.VALIDATION_SET_SIZE));    

random.shuffle(data);

validationData = [];
trainingData = [];

for i in range(0, len(data)):
    x = asInputVector(data[i][0]);
    y = asOutputVector(data[i][1]);
    # First populate validation data, then - training data
    if i < config.VALIDATION_SET_SIZE:
        validationData.append((x, y));
    else:
        trainingData.append((x, y));

network = Network([config.FRAGMENT_SIZE[0]*config.FRAGMENT_SIZE[1], 128, 64, 3]);
network.SGD(trainingData, 50, 100, 0.5, test_data=validationData if config.LIVE_VALIDATION else None);
correctPredictions = network.evaluate(validationData);
totalPredictions = len(validationData);
successRate = correctPredictions / totalPredictions;
print("Resulting success rate: %d/%d (%f%%)" % (correctPredictions, totalPredictions, successRate*100.0));

if (not os.path.isfile(config.NETWORK_FILENAME)) or yesno("%s already exists. Overwrite?"):
    saveNeuralNetwork(network, config.NETWORK_FILENAME);
