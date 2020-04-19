#!/usr/bin/env python
#translating english to hindi

import codecs
import sys
from collections import defaultdict
from nltk import word_tokenize
from tqdm import tqdm, tnrange, tqdm_notebook
from time import sleep
from operator import itemgetter

#initialize corpus
file_eng = codecs.open("train.en", "r", "utf-8")
file_hin = codecs.open("train.hi", "r", "utf-8")

corpus = dict()
# a = int(len(file_eng.readlines()))
num_sentences = 49398

print("Loading data")
pbar = tqdm(total = num_sentences)
i = 0
while i < num_sentences:
    sent1 = tuple(word_tokenize("NULL " + file_eng.readline().strip("\n")))
    sent2 = tuple(word_tokenize("NULL " + file_hin.readline().strip("\n")))
    corpus[sent1] = sent2
    i+=1
    pbar.update(1)
pbar.close()
print("\n")
##########################################

#intialize t(f|e) uniformly
num_hindi_words = len(set(hin_word for (eng_sent, hin_sent) in corpus.items() for hin_word in hin_sent))
t = defaultdict(lambda: float(1/num_hindi_words))
##########################################

#training model
# while(not converged)
print("Training translation model")
pbar2 = tqdm(total = 16)
for i in range(16):
    count_e_given_f = defaultdict(float)
    total = defaultdict(float)
    sentence_total =  defaultdict(float)
    for (eng_sent, hin_sent) in corpus.items():
        for e_word in eng_sent:
            sentence_total[e_word] = 0

            for hin_word in hin_sent:
                sentence_total[e_word] += t[(e_word,hin_word)]
        
        for e_word in eng_sent:
            for hin_word in hin_sent:
                count_e_given_f[(e_word, hin_word)] += (t[(e_word, hin_word)]/sentence_total[e_word])
                total[hin_word] += (t[(e_word, hin_word)]/sentence_total[e_word])

    for (e_word, hin_word) in count_e_given_f:
        t[(e_word, hin_word)] = count_e_given_f[(e_word, hin_word)]/total[hin_word]
    
    pbar2.update(1)
pbar2.close()
print("\n")
###########################################

#printing
iterations = 0
for ((e_word, hin_word), value) in sorted(t.items(), key=itemgetter(1), reverse=True):
    if iterations < 20:
        print("{:<20}{:>20.2}".format("t(%s|%s)" %(e_word, hin_word), value))
    else:
        break
    iterations += 1


