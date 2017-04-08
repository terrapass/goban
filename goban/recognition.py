#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:48:15 2017

@author: taras
"""
import numpy as np;

from goban.board import CellType
from goban.vision.segmentation import Segmentation
from goban.nnutils import interpret, asInputVector, ConfidenceMeasure
from random import uniform as rand

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
                rawBoard[i,j], confidence = self.__classify(segmentation[(i,j)]);
                sumConfidence += confidence;
        board = np.vectorize(CellType)(rawBoard);
        avgConfidence = sumConfidence / (self.boardWidth * self.boardHeight);
        return board, avgConfidence;

    def estimateConfidence(self, topdownBoardImage, samples = None):
        segmentation = Segmentation(topdownBoardImage, self.boardHeight, self.boardWidth);
        sumConfidence = 0.0;

        if samples == None:
            # Classify all segments and return average confidence
            for i in range(0, self.boardHeight):
                for j in range(0, self.boardWidth):
                    # Classify using network
                    sumConfidence += self.__classify(segmentation[i,j])[1];
            avgConfidence = sumConfidence / (self.boardWidth * self.boardHeight);
        else:
            # Take the requested number of random fragments and
            # return average confidence of just their classification
            #minConfidence = 1.0;
            for k in range(0, samples):
                i = int(rand(0, self.boardWidth - 1))
                j = int(rand(0, self.boardHeight - 1))
                # Classify using network
                sumConfidence += self.__classify(segmentation[(i,j)])[1];
#                if confidence < minConfidence:
#                    minConfidence = confidence;
            avgConfidence = sumConfidence / samples;
            #return board, avgConfidence - minConfidence
        return avgConfidence;
    
    def __classify(self, fragment, confidenceMeasure = ConfidenceMeasure.MAX_OUTPUT):
        # Classify using network
        classification = interpret(self.network.feedforward(asInputVector(fragment)), 0.0, confidenceMeasure)
        cellTypeValue, confidence = classification[0].value, classification[1];
        return cellTypeValue, confidence
