from heapq import nlargest
import json
from matplotlib import pyplot as plt
import os
import statistics
from collections import Counter
import numpy as np

print(os.getcwd())

# This function converts a JSON of typically model scores to a bar chart
def json_to_bar(path, N):
    with open(path) as json_file:
        dic = json.load(json_file)
        n_largest = nlargest(N, dic, key = dic.get)
        keys = n_largest
        values = [dic[n] for n in n_largest]
        plt.bar(keys, values)
        plt.show()

# This function converts a JSON of posts + associated subreddit into
# subreddit counts
def json_to_frequency(path):
    with open(path) as json_file:
        dic = json.load(json_file)
        counts = Counter(dic.values())
        tuples = [(key, val) for key, val in counts.items()]
        sorted_tuples = sorted(tuples, key = lambda x:x[0], reverse = True)
        x, y = zip(*sorted_tuples)
        plt.yscale('log')
        plt.xscale('log')
        plt.plot(x, y)
        plt.ylabel("# of subreddits")
        plt.xlabel("subreddit size")
        plt.show()

# This functions prints the mean/mean of a json file with keys + counts
# This file was under on subreddit counts.
def json_stats(path):
    with open(path) as json_file:
        dic = json.load(json_file)
        cleaned_dic = dic
        # cleaned_dic = {key:val for key, val in dic.items() if val >= 10}

        mean = sum(cleaned_dic.values()) / len(cleaned_dic)
        print(mean)
        median = statistics.median(cleaned_dic.values())
        print(median)

# This function plots takes in a json of temps x scores 
# It plots the avg SS/BLEU scores vs temp
def model_avg_graphs(path):
    scores = None
    with open(path, 'r') as f:
        scores = json.load(f)
    start_temp = 0.8
    y = scores
    x = (np.arange(len(y)) / 10) + start_temp
    plt.plot(x, y)
    plt.title("DialoGPT Temperature vs SS")
    plt.ylabel("Average SS score")
    plt.xlabel("Temperature")
    plt.show()

# This function takes in a json of temps x scores
# It plots the distribution of SS/BLEU scores in a specific temperature
def model_distributions(path, outputs_path):
    scores = None
    volatile = []
    temp = 0
    with open(path, 'r') as f:
        scores = json.load(f)
    scores = scores[temp]
    for i in range(len(scores)):
        if scores[i] < 0.15:
            print(i)
            volatile.append(i)
    print(len(volatile))
    with open(outputs_path, 'r') as output_f:
        outputs = json.load(output_f)
    for i in volatile:
        print(outputs[temp][i])
    plt.hist(scores, bins = 50)
    plt.title("Dialogpt SS distribution, Temp = 0.3")
    plt.ylabel("# Samples")
    plt.xlabel("SS score")
    plt.show()


if __name__ == "__main__":
    path = "../data/jsons/dialogpt_ss_pairwise_avgs.json"
    outputs_path = "../data/jsons/dialogpt_pairwise_outputs.json"
    model_distributions(path, outputs_path)