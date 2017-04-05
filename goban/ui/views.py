#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:07:24 2017

@author: taras
"""

import cv2;

from goban.board import CellType;

class AbstractBoardView:
    #def show(self):
        #raise NotImplementedError("show() not implemented");
    #def hide(self):
        #raise NotImplementedError("hide() not implemented");
    def update(self, board):
        raise NotImplementedError("update(board) not implemented");
        
class ConsoleBoardView:
    def update(self, board):
        # Print board
        for y in range(0,board.shape[0]):
            for x in range(0,board.shape[1]):
                if board[y][x] == CellType.BLACK:
                    print('B ',end='');
                elif board[y][x] == CellType.WHITE:
                    print('W ',end='');
                else:
                    print('+ ',end='');
            print();
