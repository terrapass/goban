#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 22:35:45 2017

@author: taras
"""

from goban.ui.dialogs import AskCornersDialog
from goban.math.geometry import sortPointsCW
from goban.corners.genetic import GeneticAlgorithmRunner, GeneticCornerDetectionAlgorithmImpl

class AbstractBoardCornerDetector:
    def findBoardCorners(self, img):
        raise NotImplementedError("findBoardCorners(img) not implemented");

class ManualBoardCornerDetector(AbstractBoardCornerDetector):
    def __init__(self, uiCornerColor = (0, 255, 0)):
        self.uiCornerColor = uiCornerColor;

    def findBoardCorners(self, img):
        return sortPointsCW(AskCornersDialog(img, self.uiCornerColor).run())

class GeneticBoardCornerDetector(AbstractBoardCornerDetector):
    def __init__(self, recognizer, generations, populationSize, mutationRate = 0.01):
        self.recognizer = recognizer;
        self.generations = generations;
        self.populationSize = populationSize;
        self.mutationRate = mutationRate;

    def findBoardCorners(self, img):
        return GeneticAlgorithmRunner(GeneticCornerDetectionAlgorithmImpl(img, self.recognizer, 2500, 0.7), self.populationSize, self.mutationRate, self.generations).run();
