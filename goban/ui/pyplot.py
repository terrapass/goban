#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt

def plotImage(img, formatString = 'gray'):
    plt.imshow(img, 'gray');
    plt.show();
