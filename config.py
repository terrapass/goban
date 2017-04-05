#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:35:12 2017

@author: taras
"""

# Whether to use camera or load image from file for labelling and recognition
USE_CAMERA = False;

# If USE_CAMERA == False, load image from this file
IMAGE_FILENAME = "/media/taras/common/Projects/OpenCV/resources/images/goban/005.jpg"

NETWORK_FILENAME = "network.json"
DATA_FILENAME = "data.json"

BOARD_WIDTH = 13;
BOARD_HEIGHT = 13;

FRAGMENT_SIZE = (32,32);

TRAINING_ADD_ROTATIONS = False;
TRAINING_ADD_FLIPS = True;

VALIDATION_SET_SIZE = 1000;

LIVE_VALIDATION = True;
