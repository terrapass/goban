#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2;

from goban.io import loadNeuralNetwork;
from goban.ui.dialogs import AskCornersDialog;
from goban.ui.views import ConsoleBoardView;
from goban.vision.operations import rectifyPerspective;
from goban.ui.cv import popupImage;
from goban.recognition import NeuralTopdownFixedSizeBoardRecognizer;
from goban.vision.operations import bgrToGray, getChannel, bgrToHsv;

import config
from mainutils import getInputImage

img = getInputImage();

cornerPoints = AskCornersDialog(img, (0, 255, 0)).run()

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

network = loadNeuralNetwork(config.NETWORK_FILENAME);
recognizer = NeuralTopdownFixedSizeBoardRecognizer(network, config.BOARD_WIDTH, config.BOARD_HEIGHT);
board, confidence = recognizer.recognize(topdownImg);

print("Recognized the following board position with avg. confidence %f" % confidence);
ConsoleBoardView().update(board);

cv2.waitKey();
