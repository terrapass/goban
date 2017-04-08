#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2;

from goban.io import loadNeuralNetwork;
from goban.ui.views import ConsoleBoardView;
from goban.vision.operations import rectifyPerspective;
from goban.ui.cv import popupImage;
from goban.recognition import NeuralTopdownFixedSizeBoardRecognizer;
from goban.vision.operations import bgrToGray, getChannel, bgrToHsv;

import config
from mainutils import getInputImage, getCornerDetector, getBoardRecognizer

img = getInputImage();
#resizedImg = cv2.resize(img, (160, 120));
cornerPoints = getCornerDetector().findBoardCorners(img);
# TODO: Encapsulate selected quadrangle display
cornerImg = img.copy();
for i in range(0, len(cornerPoints)):
    n = (i + 1) % 4;
    cv2.line(cornerImg, cornerPoints[i], cornerPoints[n], (0, 255, 0), 2);
#popupImage("Selected quadrangle", cornerImg, True);

# TODO: Encapsulate and avoid code duplication w/ genetic.py
RECTIFIED_SIZE = (config.BOARD_HEIGHT * config.FRAGMENT_SIZE[0], config.BOARD_WIDTH * config.FRAGMENT_SIZE[1]);
PADDING_WIDTH = int(RECTIFIED_SIZE[1] / (2*config.BOARD_WIDTH));
PADDING_HEIGHT = int(RECTIFIED_SIZE[0] / (2*config.BOARD_HEIGHT));

topdownImg = rectifyPerspective(img, cornerPoints, RECTIFIED_SIZE, PADDING_HEIGHT, PADDING_WIDTH);
popupImage("Rectified perspective", topdownImg, True);

#topdownImgSaturation = getChannel(bgrToHsv(topdownImg), 1);
#popupImage("Rectified perspective (saturation)", topdownImgSaturation, True);

# Convert topdown image to grayscale
topdownImg = bgrToGray(topdownImg);
#popupImage("Rectified perspective (grayscale)", topdownImg, True);

recognizer = getBoardRecognizer();
board, confidence = recognizer.recognize(topdownImg);

print("Recognized the following board position with avg. confidence %f" % confidence);
ConsoleBoardView().update(board);

cv2.waitKey();
