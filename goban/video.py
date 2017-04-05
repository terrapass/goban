#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:48:27 2017

@author: taras
"""

import cv2;

def takePicture(camIndex = 0):
    cam = cv2.VideoCapture(camIndex)
    success, img = cam.read()
    cam.release()
    if not success:
        raise IOError("Failed to take picture from camera %d");
    return img;
