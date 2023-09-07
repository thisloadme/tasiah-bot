from gensim.models import Word2Vec
from nltk import word_tokenize
import csv

EMBEDDING_DIM = 100

sentences = []

tags_responses = {}
with open('responses.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for row in csv_reader:
        tags_responses[row[0]] = row[1]
        sentences.append(word_tokenize(row[1]))

tags_patterns = {}
with open('patterns.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for idx,row in enumerate(csv_reader):
        tag_ = row[0].replace('\ufeff', '')
        if tag_ not in tags_patterns:
            tags_patterns[tag_] = []
        
        tags_patterns[tag_].append(row[1])
        sentences.append(word_tokenize(row[1]))

with open('default_dictionary.txt', encoding='utf-8') as f:
    dataset = f.readlines()
    for row in dataset:
        rowdata = row.split('<pemisah>')
        judul = rowdata[0]
        konten = rowdata[1]
        sentences.append(word_tokenize(judul))
        sentences.append(word_tokenize(konten))

# train model
model = Word2Vec(sentences, min_count=1, epochs=20, vector_size=EMBEDDING_DIM)

words = list(model.wv.index_to_key)

new_embed = []
for w in words:
    new_embed.append(w + ' ' + ' '.join([str(v) for v in model.wv.get_vector(w)]))

with open('prepared_embedding.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_embed))