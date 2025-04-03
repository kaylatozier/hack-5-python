#!/usr/bin/env python

"""
Wright-Fisher model to simulate random genetic drifts in generations of populations
"""

import random
import requests
import argparse
import numpy as np
import pandas as pd

class Population: #defining a population class instead of a bunch of functions for better efficiency and organization
    def __init__(self, N=10, f=0.2, with_np = False): #initializing the population with N and f
        self.N = N
        self.f = f
        self.with_np = with_np #allows you to switch between numpy arrays and python lists
        alleles = round(N*f) #total number of alleles in the initial population (N*f)
        self.pop = [0] * (N - alleles) + [1] * alleles #creating a self.pop list with the number of 1s determined by frquenecy f, just like in our original function

        if with_np:
            self.pop = np.array(self.pop) # converts to a NumPy array if with_np=True
            
    def __repr__(self): #function that returns the self object (population) as a string with Population(N=#, f=#) for formatting purposes
        return f"Population(N={self.N}, f={self.f})"

    def step(self, ngens=1): #now simulating one or more generations with the initialized population, just like we did in the original code but using self.pop instead and using self.N
        for i in range(ngens):
            if self.with_np:
                self.pop = np.random.choice(self.pop, size=self.N) #numpy array version of random sampling
            else:
                self.pop = random.choices(self.pop, k=self.N) #python list version

    def newfreq(self):
        return sum(self.pop)/self.N #calculated the new frequency of alleles by taking the sum of 1s in the new population and dividing it by the length of that population
        

def wfsimulation(N, f, ngens, verbose=False, outfile=None, with_np=False):
    p = Population(N, f, with_np)
    for i in range(ngens):
        freq = sum(p.pop)/p.N #calculates the sum of the alleles in a population divided by the population size to test for extinction or fixation

        if verbose:
            print(f"Generation {i}: f={freq:.1f} allele frequency")\

        if freq == 0.0:
            if verbose:
                print(f"Allele extinct at generation {i}. Simulation stopped.")
                break  # Stop if the allele is extinct

        if freq == 1.0:
            if verbose:
                print(f"Allele fixed at generation {i}. Simulation stopped.")
                break  # Stop if the allele is fixed
        p.step()
    print(f"Final Population: {p.pop}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # input population size
    parser.add_argument("-N","--popsize",type = int, help = "initial population size", default = 10)
    # input frequency of allele
    parser.add_argument("-f","--freq", type = float, help = "initial allele frequency", default = 0.2)
    # input number of generation runs
    parser.add_argument("-n", "--ngens", type = int, help = "number of generations", default = 10)
    # increasing verbosity to show the frequency of the allele in each generation run until the allele is extinct or fixed and how many generations that took
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Increase verbosity output to show extinction or fixation and allele frequency in each run")
    # runs the simulation using NumPy arrays instead of standard lists
    parser.add_argument("-np", "--with_np", action = "store_true", help = "Compute using NumPy array")

    args = parser.parse_args()
    wfsimulation(args.popsize, args.freq, args.ngens, args.verbose, args.with_np)
