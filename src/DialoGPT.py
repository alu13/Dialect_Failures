import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

import torch
import csv
import pandas as pd
import json
import time

device = 'cuda' if torch.cuda.is_available else 'cpu'
# device = 'cpu'
print("device = " + str(device))

standard_path = '../data/csvs/reddit_filtered.csv'
perturbed_path = '../data/csvs/reddit_filtered.csv'
standard_df = pd.read_csv(standard_path, index_col = 0)
perturbed_df = pd.read_csv(perturbed_path, index_col = 0)

standard_contexts = standard_df['context']
perturbed_contexts = perturbed_df['context']
short_contexts = standard_df['context'][0:10]

Dialogpt_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
Dialogpt_tokenizer.add_special_tokens({'pad_token': '<|endoftext|>'})
Dialogpt_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large").to(device=device)

def get_dialogpt_outputs(num_samples, num_copies, temp):
  # Test out how long the function takes
  start_time = time.time()
  batch_size = 10
  all_outputs = []
  for step in tqdm(range(batch_size, num_samples + 1, batch_size)):
      outputs = []
      # pull the batched inputs + append EOS token to the end of each input
      inputs = list(standard_contexts[step - batch_size:step])
      inputs = [i + Dialogpt_tokenizer.eos_token for i in inputs]

      # encode the inputs
      input_info = Dialogpt_tokenizer(inputs, padding = True, return_tensors = 'pt').to(device=device)
      input_ids = input_info['input_ids']
      attention_mask = input_info['attention_mask']

      # generated a num_samples * num_copies responses
      chat_history_ids = Dialogpt_model.generate(
          input_ids, 
          max_length=1000, 
          do_sample = True,
          # top_k=50, 
          # top_p=0.95,
          temperature = temp,
          num_return_sequences = num_copies,
          pad_token_id = Dialogpt_tokenizer.eos_token_id,
          attention_mask = attention_mask)
      # output = Dialogpt_tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
      for i in chat_history_ids:
        output = Dialogpt_tokenizer.decode(i[input_ids.shape[-1]:], skip_special_tokens=True)
        # print(output)
        outputs.append(output)
        # pretty print last ouput tokens from bot
        # print("Input: " + str(standard_contexts[step]))
        # print("DialoGPT: {}".format(Dialogpt_tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)))
      outputs = [outputs[x : x+num_copies] for x in range(0, len(outputs), num_copies)]
      all_outputs.extend(outputs)
      print("Took " + str(time.time() - start_time) + " seconds to run")
  return all_outputs

if __name__ == "__main__":
    print(get_dialogpt_outputs(10, 10, 1))