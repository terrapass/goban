#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:42:22 2017

@author: taras
"""

import cv2;

from goban.io import loadTrainingData, saveTrainingData;
from goban.ui.dialogs import AskCornersDialog, LabelingDialog;
from goban.vision.operations import rectifyPerspective;
from goban.ui.cv import popupImage;
from goban.vision.operations import bgrToGray;
from goban.vision.segmentation import Segmentation;

import config
from mainutils import getInputImage

img = getInputImage();

data = loadTrainingData(config.DATA_FILENAME, config.FRAGMENT_SIZE);

cornerPoints = AskCornersDialog(img, (0, 255, 0)).run()

RECTIFIED_SIZE = (config.BOARD_HEIGHT * config.FRAGMENT_SIZE[0], config.BOARD_WIDTH * config.FRAGMENT_SIZE[1]);
PADDING_WIDTH = int(RECTIFIED_SIZE[1] / (2*config.BOARD_WIDTH));
PADDING_HEIGHT = int(RECTIFIED_SIZE[0] / (2*config.BOARD_HEIGHT));

topdownImg = rectifyPerspective(img, cornerPoints, RECTIFIED_SIZE, PADDING_HEIGHT, PADDING_WIDTH);
popupImage("Rectified perspective", topdownImg, True);

# Convert topdown image to grayscale
topdownImg = bgrToGray(topdownImg);

topdownSegmentation = Segmentation(topdownImg, config.BOARD_WIDTH, config.BOARD_HEIGHT, config.FRAGMENT_SIZE);
labeledData = LabelingDialog(topdownSegmentation).run();

print("Labeled %d new data items" % len(labeledData));

data = data + labeledData;

saveTrainingData(data, config.DATA_FILENAME);

cv2.waitKey();
