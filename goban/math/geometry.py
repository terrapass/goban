#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:35:01 2017

@author: taras
"""
from math import atan2

def lineCoefs(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def segmentIntersection(s1p1, s1p2, s2p1, s2p2):
    minX = min(s1p1[0], s1p2[0])#, s2p1[0], s2p2[0]);
    maxX = max(s1p1[0], s1p2[0])#, s2p1[0], s2p2[0]);
    minY = min(s1p1[1], s1p2[1])#, s2p1[1], s2p2[1]);
    maxY = max(s1p1[1], s1p2[1])#, s2p1[1], s2p2[1]);

    inter = intersection(lineCoefs(s1p1, s1p2), lineCoefs(s2p1, s2p2));
    if (not inter) or (inter[0] < minX) or (inter[0] > maxX) or (inter[1] < minY) or (inter[1] > maxY):
        if inter:
            print("Truncate");
        return False;
    else:
        return inter;

def meanPoint(points):
    result = (0,0);
    for point in points:
        result = (result[0] + point[0], result[1] + point[1]);
    return (result[0]/len(points),result[1]/len(points));
    
def sqDist(point1, point2):
    return (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2;

def sortPointsCW(points):
    center = meanPoint(points);
    return sorted(points, key=lambda p: atan2(p[1] - center[1], p[0] - center[0]));
