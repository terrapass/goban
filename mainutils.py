#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:45:39 2017

@author: taras
"""

from goban.video import takePicture
from goban.io import loadImage

import config

def getInputImage():
    if config.USE_CAMERA:
        return takePicture(1);
    else:
        return loadImage(config.IMAGE_FILENAME);

def atexitWorkaround():
    # Workaround for IPython not calling atexit()
    try:
        __IPYTHON__
        cv2.waitKey();
    except NameError:
        pass;
