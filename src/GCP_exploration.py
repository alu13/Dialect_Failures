# Import the Google Cloud client library and JSON library
from google.cloud import storage
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
# Instantiate a Google Cloud Storage client and specify required bucket and file
storage_client = storage.Client()
bucket_name = "reddit_dataset_storage"
bucket = storage_client.get_bucket(bucket_name)
# Download the contents of the blob as a string and then parse it using json.loads() method
# @param num_files: The number of files that you want to pull. 0 - 1000
# @returns nothing. Saves subreddit data as a json
def get_subreddits(num_files):
    counts = {}
    for i in tqdm(range(num_files)):
        formatted_i = format(i, '05d')
        print(formatted_i)
        test_path = "reddit/20220210/test-" + formatted_i + "-of-01000.json" # Make i 4 digits regardless
        train_path = "reddit/20220210/train-" + formatted_i + "-of-01000.json"
        test_data = bucket.blob(test_path).download_as_text()
        train_data = bucket.blob(train_path).download_as_text()
        try:
            test_list = [json.loads(l) for l in test_data.splitlines()]
            train_list = [json.loads(l) for l in train_data.splitlines()]
            full_list = test_list + train_list

            for line in full_list:
                subreddit = line['subreddit']
                if subreddit not in counts:
                    counts[subreddit] = 0
                counts[subreddit] += 1
        except:
            print("readline bug")
            continue
    save_as_json(counts, "subreddit_counts")

# @param num_files: The number of files that you want to pull. 0 - 1000
# @returns nothing. Saves context data as a csv
def get_contexts(num_files):
    contexts = []
    labels = ['context', 'subreddit']
    for i in tqdm(range(num_files)):
        formatted_i = format(i, '05d')
        print(formatted_i)
        test_path = "reddit/20220210/test-" + formatted_i + "-of-01000.json" # Make i 4 digits regardless
        train_path = "reddit/20220210/train-" + formatted_i + "-of-01000.json"
        test_data = bucket.blob(test_path).download_as_text()
        train_data = bucket.blob(train_path).download_as_text()
        try:
            test_list = [json.loads(l) for l in test_data.splitlines()]
            train_list = [json.loads(l) for l in train_data.splitlines()]
            full_list = test_list + train_list

            for line in full_list:
                subreddit = line['subreddit']
                context = line['context']
                contexts.append([context, subreddit])
        except:
            print("readline bug")
            continue
    save_as_csv(contexts, labels, 'subreddit_csv')

def save_as_json(data, name):
    data_json = json.dumps(data)
    f = open(name + ".json","w")
    f.write(data_json)
    f.close()
def save_as_csv(data, labels, name):
    df = pd.DataFrame(data, columns=labels)
    df.to_csv(name + ".csv")
if __name__ == "__main__":
    get_contexts(2)