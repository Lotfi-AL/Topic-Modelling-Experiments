from nltk import word_tokenize

from utils.stats import word_frequency
import numpy as np
from nltk.corpus import stopwords


def get_stopwords():
    stopwords = []
    with open("stopwords.txt", "r", encoding="utf-8") as file:
        for line in file:
            stopwords.append(line.strip())
    return stopwords


def get_vocabulary(docs):
    '''
    This version of get_vocabulary takes 0.08 seconds on 100,000 documents whereas the old version took forever.
    '''
    vocab = []
    for i in range(0, len(docs)):
        vocab.extend(docs[i])
    return list(set(vocab))


def count_stopwords(d, stopwords):
    c = 0
    for w in d:
        if w in stopwords:
            c += 1
    return c


def get_data_stats(dataset):
    tokenized_dataset = []
    for item in dataset:
        word_tokens = word_tokenize(item)
        tokenized_dataset.append(word_tokens)
    dataset = tokenized_dataset
    dataset_size = len(dataset)
    vocab = get_vocabulary(dataset)
    vocab_size = len(vocab)
    freq = {}
    freq = word_frequency(freq, dataset)
    avg_token_freq = np.mean([freq[x] for x in freq.keys()])
    doc_lengths = [len(d) for d in dataset]
    total_tokens = sum(doc_lengths)
    avg_token_per_doc = np.mean(doc_lengths)
    stopwords_list = get_stopwords()
    avg_stopwords_per_doc = np.mean([count_stopwords(d, stopwords_list) for d in dataset])
    max_tokens_in_a_doc = max(map(len, dataset))
    min_tokens_in_a_doc = min(map(len,dataset))
    return [dataset_size, vocab_size, total_tokens, avg_token_freq, avg_token_per_doc, avg_stopwords_per_doc,
            max_tokens_in_a_doc, min_tokens_in_a_doc]
