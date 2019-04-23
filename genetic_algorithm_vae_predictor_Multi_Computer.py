# from https://github.com/philippesaade11/vaelstmpredictor/blob/GeneticAlgorithm/Genetic-Algorithm.py
# python vaelstmpredictor/genetic_algorithm_vae_predictor.py ga_vae_nn_test_0 --verbose --iterations 500 --population_size 10 --num_epochs 200
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from time import time
import json
import sys
from sklearn.externals import joblib
from contextlib import redirect_stdout

from keras import backend as K
from keras.utils import to_categorical

from vaelstmpredictor.utils.model_utils import get_callbacks, init_adam_wn
from vaelstmpredictor.utils.model_utils import save_model_in_pieces
from vaelstmpredictor.utils.model_utils import AnnealLossWeight
from vaelstmpredictor.utils.data_utils import MNISTData
from vaelstmpredictor.utils.weightnorm import data_based_init
from vaelstmpredictor.vae_predictor.model import VAEPredictor
from vaelstmpredictor.vae_predictor.train import train_vae_predictor

from GeneticAlgorithm import * 

from paramiko import SSHClient, SFTPClient, Transport, AutoAddPolicy
import multiprocessing as mp

def train_generation(generation, clargs):
    machines = [{"host": "example.com", "username": "Username", "password": "Password"},
                 {"host": "example.com", "username": "Username", "password": "Password"},
                 {"host": "example.com", "username": "Username", "password": "Password"}]
    queue = mp.Queue()
    

    #Create Processes
    for machine in machines:
        queue.put(machine)

    alldone = False
    while not alldone:
        alldone = True
        for chrom in generation:
            if not chrom.isTrained:
                print("Creating Process for Chromosome "+ str(chrom.chromosomeID))
                #Find a Chromosome that is not trained yet
                alldone = False
                #Wait for queue to have a value, which is the ID of the machine that is done.
                machine = queue.get()
                process = mp.Process(target=train_chromosome, args=(chrom, machine, queue))
                process.start()

def train_chromosome(chromosome, machine, queue):
    sys.stdout = open('output'+str(chromosome.chromosomeID)+".txt", 'w')
    sys.stderr = open('error'+str(chromosome.chromosomeID)+".txt", 'w')
    
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(machine["host"], username=machine["username"], password=machine["password"])

    stdin, stdout, stderr = ssh.exec_command('ls | grep vaelstmclassifier')
    if(len(stdout.readlines()) == 0):
        #Upload Files to Machine
        print("Uploading file to machine")
        transport = Transport((machine["host"], 22))
        transport.connect(username = machine["username"], password = machine["password"])
        sftp = SFTPClient.from_transport(transport)
        sftp.put("C:/Users/Owner/Desktop/vaelstmclassifier.zip", "vaelstmclassifier.zip")
        stdin, stdout, stderr = ssh.exec_command('unzip vaelstmclassifier.zip')
        error = "".join(stderr.readlines())
        if error != "":
            print("Errors has occured while unzipping file in machine: "+str(machine)+"\nError: "+error)
                
        stdin, stdout, stderr = ssh.exec_command('cd vaelstmpredictor; ../anaconda3/envs/tf_gpu/bin/python setup.py install')
        error = "".join(stderr.readlines())
        if error != "":
            print("Errors setting up vaelstmpredictor: "+str(machine)+"\nError: "+error)
        sftp.close()
        transport.close()
        print("File uploaded")

    params = {'clargs':chromosome.clargs, 
                    'verbose':chromosome.verbose, 
                    'data_instance':chromosome.data_instance, 
                    'generationID':chromosome.generationID, 
                    'chromosomeID':chromosome.chromosomeID,
                    'vae_kl_weight':chromosome.vae_kl_weight, 
                    'dnn_weight':chromosome.dnn_weight,
                    'dnn_kl_weight':chromosome.dnn_kl_weight,
                    'vae_latent_dim':chromosome.vae_latent_dim,
                    'vae_hidden_dims':chromosome.vae_hidden_dims,
                    'dnn_hidden_dims':chromosome.dnn_hidden_dims
                   }
    
    print("Executing command")
    command = "anaconda3/envs/tf_gpu/bin/python vaelstmclassifier/run_chromosome.py \""+json.dumps(params)+"\""
    stdin, stdout, stderr = ssh.exec_command(command)
    error = "".join(stderr.readlines())
    if error != "":
        print("Errors has occured while tainging in machine: "+str(machine)+"\nError: "+error)
    if "".join(stdout.readlines()[-4:]) == "done":
        print("Trained Successfully")
    queue.put(machine)
    chromosome.isTrained = True
    print("Command Executed")
    ssh.close()
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_name', type=str, default='ga_test_',
                help='tag for current run')
    parser.add_argument('--predictor_type', type=str, default="classification",
                help='select `classification` or `regression`')
    parser.add_argument('--batch_size', type=int, default=128,
                help='batch size')
    parser.add_argument('--optimizer', type=str, default='adam',
                help='optimizer name') 
    parser.add_argument('--num_epochs', type=int, default=200,
                help='number of epochs')
    parser.add_argument('--start_small', action='store_true',
                help='Only the first hidden layer is initially populated')
    parser.add_argument('--init_large', action='store_true', 
                help='Initial the 1st layer in [num_features/2,num_features]')
    parser.add_argument('--max_vae_hidden_layers', type=int, default=5, 
                help='Maximum number of VAE hidden layers')
    parser.add_argument('--max_vae_latent', type=int, default=1024, 
                help='Maximum number of VAE neurons per layer')
    parser.add_argument('--max_dnn_latent', type=int, default=1024, 
                help='Maximum number of DNN neurons per layer')
    parser.add_argument('--max_dnn_hidden_layers', type=int, default=5,
                help='Maximum number of DNN hidden layers')
    parser.add_argument('--dnn_weight', type=float, default=1.0,
                help='relative weight on prediction loss')
    parser.add_argument('--prediction_log_var_prior', type=float, default=0.0,
                help='w log var prior')
    parser.add_argument("--do_log", action="store_true", 
                help="save log files")
    parser.add_argument("--do_chckpt", action="store_true",
                help="save model checkpoints")
    parser.add_argument('--patience', type=int, default=10,
                help='# of epochs, for early stopping')
    parser.add_argument("--kl_anneal", type=int, default=0, 
                help="number of epochs before kl loss term is 1.0")
    parser.add_argument("--w_kl_anneal", type=int, default=0, 
                help="number of epochs before w's kl loss term is 1.0")
    parser.add_argument('--log_dir', type=str, default='data/logs',
                help='basedir for saving log files')
    parser.add_argument('--model_dir', type=str, default='data/models',
                help='basedir for saving model weights')    
    parser.add_argument('--train_file', type=str, default='MNIST',
                help='file of training data (.pickle)')
    parser.add_argument('--cross_prob', type=float, default=0.7,
                help='Probability of crossover between generations')
    parser.add_argument('--mutate_prob', type=float, default=0.01,
                help='Probability of mutation for each member')
    parser.add_argument('--population_size', type=int, default=10,
                help='size of the population to evolve; '\
                        'preferably divisible by 2')
    parser.add_argument('--iterations', type=int, default=50,
                help='number of iterations for genetic algorithm')
    parser.add_argument('--verbose', action='store_true',
                help='print more [INFO] and [DEBUG] statements')
    parser.add_argument('--make_plots', action='store_true',
                help='make plots of growth in the best_loss over generations')
    
    clargs = parser.parse_args()
    
    run_name = clargs.run_name
    num_epochs = clargs.num_epochs
    cross_prob = clargs.cross_prob
    mutate_prob = clargs.mutate_prob
    population_size = clargs.population_size
    iterations = clargs.iterations
    verbose = clargs.verbose
    make_plots = clargs.make_plots

    clargs.data_type = 'MNIST'
    data_instance = MNISTData(batch_size = clargs.batch_size)
    
    n_train, n_features = data_instance.data_train.shape
    n_test, n_features = data_instance.data_valid.shape

    clargs.original_dim = n_features
    
    clargs.time_stamp = int(time())
    clargs.run_name = '{}_{}_{}'.format(clargs.run_name, 
                                clargs.data_type, clargs.time_stamp)

    if verbose: print('\n\n[INFO] Run Base Name: {}\n'.format(clargs.run_name))
    
    clargs.n_labels = len(np.unique(data_instance.train_labels))
    
    generation = generate_random_chromosomes(
                        population_size = population_size, 
                        clargs = clargs, 
                        data_instance = data_instance, TrainFunction=train_generation)

    generationID = 0    
    evolutionary_tree = {}
    evolutionary_tree[generationID] = save_generation_to_tree(generation,   
                                                            verbose=verbose)
    
    best_fitness = []
    if make_plots:
        fig = plt.gcf()
        fig.show()

    start = time()
    # while gen_num < iterations:
    for _ in range(iterations):
        start_while = time()

        # Create new generation
        generationID += 1
        new_generation = []
        chromosomeID = 0
        for _ in range(population_size//2):
            parent1, parent2 = select_parents(generation)
            child1, child2, crossover_happened = cross_over(parent1, parent2, 
                                                cross_prob, verbose=verbose)
            
            child1.generationID = generationID
            child1.chromosomeID = chromosomeID; chromosomeID += 1 
            child2.generationID = generationID
            child2.chromosomeID = chromosomeID; chromosomeID += 1 
            
            child1, mutation_happened1 = mutate(child1, mutate_prob, 
                                                verbose=verbose)
            child1, mutation_happened2 = mutate(child2, mutate_prob, 
                                                verbose=verbose)
            
        train_generation(new_generation, clargs)

        print('Time for Generation{}: {} minutes'.format(child1.generationID, 
                                                (time() - start_while)//60))

        generation = new_generation
        evolutionary_tree[generationID] = save_generation_to_tree(generation,
                                                            verbose=verbose)

        best_fitness.append(max(chrom.fitness for chrom in generation))
        
        if make_plots:
            plt.plot(best_fitness, color="c")
            plt.xlim([0, iterations])
            fig.canvas.draw()

    evtree_save_name = 'evolutionary_tree_{}_ps{}_iter{}_epochs{}_cp{}_mp{}'
    evtree_save_name = evtree_save_name + '.joblib.save'
    evtree_save_name = evtree_save_name.format(run_name, population_size, 
                                iterations, num_epochs, cross_prob,mutate_prob)
    evtree_save_name = os.path.join(clargs.model_dir, evtree_save_name)

    print('[INFO] Saving evolutionary tree to {}'.format(evtree_save_name))
    joblib.dump(evolutionary_tree, evtree_save_name)
