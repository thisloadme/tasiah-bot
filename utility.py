import difflib
import os
import nltk
import json

current_dir = os.getcwd()

def is_similar(first, second):
    return difflib.SequenceMatcher(None, first, second).ratio() > 0.7

def tokenize_correct_typo_slang(sentence, all_words, remove_stop=False):
    ignore_words = ['?', '!', '<', '>', '.', ',']
    words = nltk.word_tokenize(sentence)
    if remove_stop:
        words = remove_stopwords_indo(words)
    words = [slang_word_meaning(w) for w in words if w not in ignore_words]
    for (idx, word) in enumerate(words):
        if word not in all_words:
            valid = [w for w in all_words if is_similar(word, w)]
            words[idx] = valid[0] if len(valid) > 0 else word
    
    return words

def remove_stopwords_indo(tokenized_sentence):
    with open(current_dir + '/combined_stop_words.txt', 'r') as f:
        lines = f.readlines()

    stopwords_indo = [w.replace("\n", '') for w in lines]
    return [w for w in tokenized_sentence if w not in stopwords_indo]

def slang_word_meaning(word):
    with open(current_dir + '/combined_slang_words.txt', 'r') as f:
        dict = json.load(f)
    
    return dict[word] if word in dict else word