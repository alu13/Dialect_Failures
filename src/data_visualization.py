from heapq import nlargest
import json
from matplotlib import pyplot as plt
import os
import statistics
from collections import Counter
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



path = "../data/subreddit_counts.json"
# json_to_bar("subreddit_counts.json", 8)
json_stats(path)
json_to_frequency(path)