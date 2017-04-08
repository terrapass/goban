#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:45:39 2017

@author: taras
"""

from goban.video import takePicture
from goban.io import loadImage, loadNeuralNetwork
from goban.corners.detectors import ManualBoardCornerDetector, GeneticBoardCornerDetector
from goban.recognition import NeuralTopdownFixedSizeBoardRecognizer

import config

def getInputImage():
    if config.USE_CAMERA:
        return takePicture(1);
    else:
        return loadImage(config.IMAGE_FILENAME);

__RECOGNIZER = None;

def getBoardRecognizer():
    global __RECOGNIZER;
    if __RECOGNIZER == None:
        network = loadNeuralNetwork(config.NETWORK_FILENAME);
        __RECOGNIZER = NeuralTopdownFixedSizeBoardRecognizer(network, config.BOARD_WIDTH, config.BOARD_HEIGHT);
    return __RECOGNIZER;
        
def getCornerDetector():
    if config.CORNER_DETECTION_STRATEGY == config.CornerDetectionStrategy.MANUAL:
        return ManualBoardCornerDetector();
    elif config.CORNER_DETECTION_STRATEGY == config.CornerDetectionStrategy.GENETIC:
        return GeneticBoardCornerDetector(getBoardRecognizer(), 100, 25, 0.2);
    else:
        raise NotImplementedError("Corner detection strategy %s is not currently supported" % str(config.CORNER_DETECTION_STRATEGY));

def atexitWorkaround():
    # Workaround for IPython not calling atexit()
    try:
        __IPYTHON__
        cv2.waitKey();
    except NameError:
        pass;
