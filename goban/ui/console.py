#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 22:21:52 2017

@author: taras
"""

def yesno(prompt = ""):
    yes = ["Y", "YES"];
    no = ["N", "NO"];
    while True:
        answer = input(prompt + " [Y/N]").upper();
        if answer in yes:
            return True;
        elif answer in no:
            return False;
