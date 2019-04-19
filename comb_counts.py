import itertools
import collections
import operator 
import argparse
import os.path
import pickle
from multiprocessing import Lock, Process, Manager



class PreferenceCounter():
    def __init__(self, input_file, backup_file, output_file, sigma):
        self.sigma = sigma
        self.all_overlaps = {}
        if os.path.isfile(backup_file):
            print ("backup file exist " + backup_file)
            self.process_backup_file(backup_file, output_file, sigma)
        else:
            print("backup file does not exist. Please run overlap.py first")
    def write_to_output(self, count_map_reverse, output_file, sigma):
        count_set = count_map_reverse.keys()
        count_set.sort(reverse = True)
        with open(output_file, "a") as output:
            for count in count_set:
                if count >= sigma:
                    pairs = count_map_reverse[count]
                    for pair in pairs:
                        items = ", ".join(pair)
                        output.write(str(len(pair)) + ', ' + str(count) + ', ' + items + '\n')
        print("finish processing, output file to: " + output_file)
        
    
    def process_backup_file(self, backup_file, output_file, sigma):
        count_map_reverse = pickle.load(open(backup_file, "rb"))
        self.write_to_output(count_map_reverse, output_file, sigma)
    
   
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_file", default="", type = str)
    args.add_argument("--output_file", default="", type = str)
    args.add_argument("--sigma", default = 3, type = int)
    FLAGS = args.parse_args()
    input_file = FLAGS.input_file
    print("input_file " + input_file)
    backup_file = "/".join(input_file.split('/')[:-1]) + "/tmp/"+input_file.split('/')[-1]+".pkl"
    print("backup_dir " + backup_file)
    output_file = FLAGS.output_file
    if not output_file:
        output_file = input_file + str(FLAGS.sigma) + "_output.dat"
    print("output file " + output_file)
    sigma = FLAGS.sigma
    PreferenceCounter(input_file, backup_file, output_file, sigma)

