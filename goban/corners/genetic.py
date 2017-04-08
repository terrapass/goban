#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:21:22 2017

@author: taras
"""

import cv2
import numpy as np

from random import uniform as rand

from goban.math.geometry import sortPointsCW, quadArea, interAngleCos
from goban.vision.operations import rectifyPerspective, bgrToGray

import config

class GeneticAlgorithmRunner:
    def __init__(self, impl, populationSize, mutationRate, generations):
        self.impl = impl;
        self.populationSize = populationSize;
        self.mutationRate = mutationRate;
        self.generations = generations; # TODO: Add other stopping conditions
        
    def run(self):
        population = self.impl.generatePopulation(self.populationSize);
        maxFitness = None;
        bestIndividual = None;
#        cv2.namedWindow("gen");
        for i in range(0, self.generations):
            fitness = [self.impl.calculateFitness(individual) for individual in population];
            
            maxFitnessInGeneration = max(fitness);
            bestInGeneration = population[fitness.index(maxFitnessInGeneration)];
                                          
            if (bestIndividual == None) or (maxFitnessInGeneration > maxFitness):
                maxFitness = maxFitnessInGeneration;
                bestIndividual = bestInGeneration;

            print("Generation %d best fitness: %f (%s)" % (i, maxFitnessInGeneration, str(bestInGeneration)));
#            visImg = self.impl.img.copy();
#            for individual in population:
#                for i in range(0, len(individual)):
#                    n = (i + 1) % 4;
#                    if bestInGeneration == individual:
#                        cv2.line(visImg, individual[i], individual[n], (0, 255, 0), 2);
#                    else:
#                        cv2.line(visImg, individual[i], individual[n], (0, 0, 255), 1);
#            for i in range(0, len(bestIndividual)):
#                n = (i + 1) % 4;
#                cv2.line(visImg, bestIndividual[i], bestIndividual[n], (255, 255, 0), 2);
#            cv2.imshow("gen", visImg);
#            cv2.waitKey(1);

            newPopulation = []
            for j in range(0, self.populationSize):
                parent0 = self.select(population, fitness);
                parent1 = self.select(population, fitness);
                if parent0 == parent1:
                    for r in range(0, 10):
                        parent1 = self.select(population, fitness);
                        if parent0 != parent1:
                            break;
                child = self.impl.mutate(self.impl.crossover(parent0, parent1), self.mutationRate);
                newPopulation.append(child);
            population = newPopulation;
        return bestIndividual;

    # Roulette wheel selection
    def select(self, population, fitness):
        # Random roulette wheel position
        pos = rand(0, sum(fitness));
        curPos = 0.0;
        for i, f in enumerate(fitness):
            if pos < curPos + f:
                return population[i];
            curPos += f;
        return population[len(population) - 1];        

class AbstractGeneticAlgorithmImpl:
    def generatePopulation(self, size):
        raise NotImplementedError("generatePopulation(size) not implemented");
    
    def calculateFitness(self, individual):
        raise NotImplementedError("calculateFitness(individual) not implemented");

    def crossover(self, individual0, individual1):
        raise NotImplementedError("crossover(individual0, individual1) not implemented");

    def mutate(self, individual, rate):
        raise NotImplementedError("mutate(individual, rate) not implemented");

class GeneticCornerDetectionAlgorithmImpl(AbstractGeneticAlgorithmImpl):
    def __init__(self, img, recognizer, minArea, minAbsCos):
        self.img = img;
        self.recognizer = recognizer;
        self.minArea = minArea;
        self.minAbsCos = minAbsCos;

    def generatePopulation(self, size):
        population = []
        for i in range(0, size):
            cornerPoints = []
            for j in range(0, 4):
                cornerPoints.append((int(rand(0, self.img.shape[1])), int(rand(0, self.img.shape[0]))));
            population.append(sortPointsCW(cornerPoints));
        return population;

    def calculateFitness(self, individual):
        # Check if convex
        if len(cv2.convexHull(np.array(individual))) != 4:
            return 0.01;

        # Check if bigger than the min area 
        if quadArea(individual) < self.minArea:
            return 0.01;
        
        # Check if the angles between sides are within the specified limit
        for i in range(0, 4):
            n = (i + 1) % 4;
            p = (i - 1) % 4;
            if abs(interAngleCos(individual[p], individual[i], individual[i], individual[n])) > self.minAbsCos:
                return 0.01;
        
        # Use recognizer's average confidence as fitness
        RECTIFIED_SIZE = (config.BOARD_HEIGHT * config.FRAGMENT_SIZE[0], config.BOARD_WIDTH * config.FRAGMENT_SIZE[1]);
        PADDING_WIDTH = int(RECTIFIED_SIZE[1] / (2*config.BOARD_WIDTH));
        PADDING_HEIGHT = int(RECTIFIED_SIZE[0] / (2*config.BOARD_HEIGHT));
        topdownImg = rectifyPerspective(self.img, individual, RECTIFIED_SIZE, PADDING_HEIGHT, PADDING_WIDTH);
        topdownImg = bgrToGray(topdownImg);
        avgConfidence = self.recognizer.estimateConfidence(topdownImg, 100);

        return avgConfidence;

    def crossover(self, individual0, individual1):
        dna0 = [individual0[0][0], individual0[0][1],\
                individual0[1][0], individual0[1][1],\
                individual0[2][0], individual0[2][1],\
                individual0[3][0], individual0[3][1]];
        dna1 = [individual1[0][0], individual1[0][1],\
                individual1[1][0], individual1[1][1],\
                individual1[2][0], individual1[2][1],\
                individual1[3][0], individual1[3][1]];
        
        assert len(dna0) == len(dna1);
        
        crossoverIndex = int(rand(0, len(dna0)));
        newDna = []
        for i in range(0, len(dna0)):
            newDna.append(dna0[i] if i < crossoverIndex else dna1[i]);
        
        assert len(newDna) == 8;

        return [(newDna[i], newDna[i + 1]) for i in range(0, 8, 2)];

    def mutate(self, individual, rate):
        dna = [individual[0][0], individual[0][1],\
                individual[1][0], individual[1][1],\
                individual[2][0], individual[2][1],\
                individual[3][0], individual[3][1]];
        for i in range(0, len(dna)):
            if rand(0, 1) < rate:
                dna[i] = int(rand(0, self.img.shape[1])) if (i % 2 == 0) else int(rand(0, self.img.shape[0]));
                #dna[i] = (dna[i] + (int(rand(-50,50)))) % (self.img.shape[1] if (i % 2 == 0) else self.img.shape[0]);
        
        return [(dna[i], dna[i + 1]) for i in range(0, 8, 2)];

    