from paramiko import SSHClient, SFTPClient, Transport, AutoAddPolicy
import json
import multiprocessing as mp
import sys

def train_chromosome(chromosome, machine, queue):
    sys.stdout = open('output.txt', 'w')
    sys.stderr = open('error.txt', 'w')
    
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
        sftp.close()
        transport.close()
        stdin, stdout, stderr = ssh.exec_command('unzip vaelstmclassifier.zip')
        error = "".join(stderr.readlines())
        if error != "":
            print("Errors has occured in machine: "+str(machine)+"\nError: "+error)
            
        print("File uploaded")
    params = {'clargs':1, 'verbose':"hellur"}

    print("Executing command")
    command = "python vaelstmclassifier/run_chromosome.py \""+json.dumps(params)+"\""
    stdin, stdout, stderr = ssh.exec_command(command)
    error = "".join(stderr.readlines())
    if error != "":
        print("Errors has occured while training in machine: "+str(machine)+"\nError: "+error)
    if "".join(stdout.readlines()[-4:]) == "done":
        print("Trained Successfully")
    queue.put(machine)
    ssh.close()
    print("Command Executed")

def train_generation(generation):
    machines = [{"host": "linuxdev.accbyblos.lau.edu.lb", "username": "manuella.germanos", "password": "."}]
    queue = mp.Queue()

    #Create Processes
    for machine in machines:
        queue.put(machine)

    alldone = False
    while not alldone:
        alldone = True
        for chrom in generation:
            print("Train :"+ str(chrom))
            #print("Creating Process for Chromosome "+ chrom.chromosomeID)
            #Find a Chromosome that is not trained yet
            #Wait for queue to have a value, which is the ID of the machine that is done.
            machine = queue.get()
            print("Machine :"+ str(machine))
            process = mp.Process(target=train_chromosome, args=(chrom, machine, queue))
            process.start()

if __name__ == '__main__':
    train_generation([1,2,3])
