# from https://github.com/philippesaade11/vaelstmpredictor/blob/GeneticAlgorithm/Genetic-Algorithm.py
# python vaelstmpredictor/genetic_algorithm_vae_predictor.py ga_vae_nn_test_0 --verbose --iterations 500 --population_size 10 --num_epochs 200
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from time import time, sleep
import json

from GeneticAlgorithm import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('params', type=str, default='',
                help='Chromosome Parameters')
    
    params = json.loads(parser.parse_args().params)
    print(params)
    
    chrom = Chromosome(**params)
    chrom.train()
    print("done")
