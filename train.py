import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import LSTM, Bidirectional, Dropout, Embedding
from tensorflow.keras.utils import pad_sequences
from keras.optimizers import Adam
from keras.models import Model
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import csv
import os
import json

current_dir = os.getcwd()

EMBEDDING_DIM = 100
MAX_VOCAB_SIZE = 20000
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 32
HIDDEN_SIZE = 128
EPOCHS = 500
LEARNING_RATE = 0.01
MAX_SEQ_LENGTH = 50

word2vec = {}
with open(current_dir + '/prepared_embedding.txt', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vec = np.asarray(values[1:], dtype='float32')
        word2vec[word] = vec

num_tags = 20
all_tags = {}
all_text_tags = []
with open(current_dir + '/responses.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for idx, row in enumerate(csv_reader):
        tag_ = row[0].replace('\ufeff', '')
        all_tags[tag_] = np.zeros(num_tags)
        all_tags[tag_][idx] = 1
        all_text_tags.append(tag_)

all_patterns = []
y = []
with open(current_dir + '/patterns.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for idx,row in enumerate(csv_reader):
        tag_ = row[0].replace('\ufeff', '')
        pattern_ = row[1]

        all_patterns.append(pattern_)
        y.append(all_tags[tag_])

y = np.array(y)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_patterns)

all_encoded = []
max_len_seq = 0
for encoded in tokenizer.texts_to_sequences(all_patterns):
    if len(encoded) > 0:
        all_encoded.append(encoded)
        if len(encoded) > max_len_seq:
            max_len_seq = len(encoded)

max_len_seq = min(max_len_seq, MAX_SEQ_LENGTH)

X = pad_sequences(all_encoded, maxlen=max_len_seq)

word2idx = tokenizer.word_index
idx2word = tokenizer.index_word

num_words = min(MAX_VOCAB_SIZE, len(word2idx) + 1)

embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word2idx.items():
    if i < MAX_VOCAB_SIZE:
        embedding_vector = word2vec.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(
    num_words,
    EMBEDDING_DIM,
    weights=[embedding_matrix],
    input_length=max_len_seq,
    trainable=False
)

input_ = Input(shape=(max_len_seq,))
x = embedding_layer(input_)
x = Bidirectional(LSTM(HIDDEN_SIZE, return_sequences=True))(x)
x = GlobalMaxPooling1D()(x)
output = Dense(num_tags, activation='sigmoid')(x)

model = Model(input_, output)
model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=LEARNING_RATE),
    metrics=['accuracy']
)

r = model.fit(
    X,
    y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_split=VALIDATION_SPLIT
)

plt.plot(r.history['loss'], label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

plt.plot(r.history['accuracy'], label='accuracy')
plt.plot(r.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()

p = model.predict(X)
aucs = []
for j in range(num_tags):
    auc = roc_auc_score(y[:,j], p[:,j])
    aucs.append(auc)
print(np.mean(aucs))

model.save(current_dir + '/pre_trained_model.keras')

with open(current_dir + '/train_config.json', 'w', encoding='utf-8') as f:
    array_data = {
        "input_size": max_len_seq,
        "output_size": num_tags,
        "hidden_size": HIDDEN_SIZE, 
        "all_words": num_words,
        "tags": all_text_tags,
        "targets": y.tolist(),
        "word2idx": word2idx,
        "idx2word": idx2word
    }

    json.dump(array_data, f)