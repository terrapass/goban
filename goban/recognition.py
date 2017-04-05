#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:48:15 2017

@author: taras
"""
import numpy as np;

from goban.board import CellType
from goban.vision.segmentation import Segmentation
from goban.nnutils import interpret, asInputVector

class AbstractBoardRecognizer:
    def recognize(boardImage):
        raise NotImplementedError("recognize() not implemented");

class NeuralTopdownFixedSizeBoardRecognizer(AbstractBoardRecognizer):
    def __init__(self, network, boardWidth, boardHeight):
        self.network = network;
        self.boardWidth = boardWidth;
        self.boardHeight = boardHeight;
        
    def recognize(self, topdownBoardImage):
        rawBoard = np.int8(np.zeros((self.boardWidth, self.boardHeight)));
        segmentation = Segmentation(topdownBoardImage, self.boardHeight, self.boardWidth);
        sumConfidence = 0.0;
        for i in range(0, self.boardHeight):
            for j in range(0, self.boardWidth):
                # Classify using network
                classification = interpret(self.network.feedforward(asInputVector(segmentation[(i,j)])))
                rawBoard[i,j], confidence = classification[0].value, classification[1];
                sumConfidence += confidence;
        board = np.vectorize(CellType)(rawBoard);
        avgConfidence = sumConfidence / (self.boardWidth * self.boardHeight);
        return board, avgConfidence;
