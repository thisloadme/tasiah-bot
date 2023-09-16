import tensorflow as tf
from keras.models import load_model
import json
import os
from sklearn.metrics import roc_auc_score
from tensorflow.keras.utils import pad_sequences
import numpy as np
import csv
import random
from utility import tokenize_correct_typo_slang

current_dir = os.getcwd()

MAX_SEQ_LENGTH = 50

model = load_model(current_dir + '/pre_trained_model.keras')

config = []
with open(current_dir + '/train_config.json', encoding='utf-8') as f:
    config = json.load(f)

input_size = config['input_size']
output_size = config['output_size']
hidden_size = config['hidden_size']
all_words = config['all_words']
tags = config['tags']
targets = np.array(config['targets'])
word2idx = config['word2idx']
idx2word = config['idx2word']

removed_char = ['?', '!']

def get_response(message):
    message_ori = ' '.join(tokenize_correct_typo_slang(message, idx2word.values()))
    message = ' '.join(tokenize_correct_typo_slang(message, idx2word.values(), True))
    encoded = [word2idx[s] if s in word2idx else 0 for s in message.strip().lower().split() if s not in removed_char]

    if len(encoded) > MAX_SEQ_LENGTH:
        return 'Maaf atas keterbatasan saya, tapi saya hanya bisa menerima maksimal 50 kata dalam satu pertanyaan'

    X = pad_sequences([encoded], maxlen=input_size)

    pred = model.predict(X)
    pred_idx = np.argmax(pred)
    pred_tags = tags[pred_idx]

    response = ''
    
    base_resp = []
    with open(current_dir + '/basic_response.json', encoding='utf-8') as f:
        base_resp = json.load(f)

    if np.max(pred) > 0.7:

        random_number = random.randint(1, 100)
        if random_number <= 60:
            response = response + random.choice(base_resp['pembukaan']).replace('<replaced>', '"' + (message_ori.capitalize()) + '"')

        with open(current_dir + '/responses.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                if row[0] == pred_tags:
                    response = response + row[1]

        random_number = random.randint(1, 100)
        if random_number <= 40:
            response = response + random.choice(base_resp['penutupan'])
    else:
        response = random.choice(base_resp['tidak_tahu'])

    return response

bot_name = 'Tasiah'

if __name__ == '__main__':
    while True:
        message = input('Kamu: ')
        if message == 'quit':
            break

        resp = get_response(message)
        
        print(bot_name + ': ' + resp)