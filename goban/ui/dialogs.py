#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:07:24 2017

@author: taras
"""

import cv2;

from goban.ui.cv import *
from goban.ui.pyplot import *
from goban.board import CellType

class AbstractDialog:
    def run(self):
        raise NotImplementedError("run() is not implemented");

class AskCornersDialog(AbstractDialog):
    CORNER_SELECTION_WINDOW = 'Select board corners';
    
    def __init__(self, img, cornerColor):
        self.img = img;
        self.cornerColor = cornerColor;
        
    def run(self):
        cornerPoints = []
        def onMouseEvent(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONUP:
                cornerPoints.append((x, y));
            elif event == cv2.EVENT_RBUTTONDOWN:
                cornerPoints.pop();
    
        cv2.namedWindow(AskCornersDialog.CORNER_SELECTION_WINDOW);
        cv2.setMouseCallback(AskCornersDialog.CORNER_SELECTION_WINDOW, onMouseEvent);
    
        while len(cornerPoints) < 4:
            cornsel_img = self.img.copy();
            for cornerPoint in cornerPoints:
                cv2.circle(cornsel_img, cornerPoint, 1, (0, 255, 0), 3);
            cv2.imshow(AskCornersDialog.CORNER_SELECTION_WINDOW, cornsel_img);
            cv2.waitKey(1);
        cv2.destroyWindow(AskCornersDialog.CORNER_SELECTION_WINDOW);

        return cornerPoints;

class LabelingDialog(AbstractDialog):
    PROMPT = "Class (0 - empty, 1 - black, 2 - white, ENTER - skip)? ";

    def __init__(self, segmentation):
        self.segmentation = segmentation;
    
    def run(self):
        data = [];
        for fragment in self.segmentation:
            # Ask to classify
            plotImage(fragment, 'gray');
            inputStr = input(LabelingDialog.PROMPT);
            try:
                data.append((fragment, CellType(int(inputStr))));
            except ValueError:
                print("Skipped.");
        return data;
