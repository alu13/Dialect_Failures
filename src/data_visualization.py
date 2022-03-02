from heapq import nlargest
import json
from matplotlib import pyplot as plt
import os
import statistics
from collections import Counter
import numpy as np
print(os.getcwd())
def json_to_bar(path, N):
    with open(path) as json_file:
        dic = json.load(json_file)
        n_largest = nlargest(N, dic, key = dic.get)
        keys = n_largest
        values = [dic[n] for n in n_largest]
        plt.bar(keys, values)
        plt.show()
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
def json_stats(path):
    with open(path) as json_file:
        dic = json.load(json_file)
        cleaned_dic = dic
        # cleaned_dic = {key:val for key, val in dic.items() if val >= 10}

        mean = sum(cleaned_dic.values()) / len(cleaned_dic)
        print(mean)
        median = statistics.median(cleaned_dic.values())
        print(median)
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
def model_distributions(path):
    scores = None
    with open(path, 'r') as f:
        scores = json.load(f)
    temp = scores[4]
    plt.hist(temp, bins = 50)
    plt.title("BlenderBot SS distribution, Temp = 1.2")
    plt.ylabel("# Samples")
    plt.xlabel("SS score")
    plt.show()


path = "../data/blenderbot_ss_scores.json"
model_distributions(path)