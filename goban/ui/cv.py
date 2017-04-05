#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2;
import atexit;

__ENABLE_IMAGE_POPUPS = False;

def enableImagePopups(value = True):
    global __ENABLE_IMAGE_POPUPS;
    __ENABLE_IMAGE_POPUPS = value;

def popupImage(title, image, force=False):
    if __ENABLE_IMAGE_POPUPS or force:
        cv2.imshow(title, image);
        atexit.unregister(cv2.waitKey);
        atexit.register(cv2.waitKey);
