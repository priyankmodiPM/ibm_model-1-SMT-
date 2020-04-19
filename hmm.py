#!/usr/bin/env python
import sys
import time
from collections import defaultdict
import pickle
import codecs
from numpy import *
from tqdm import tqdm, tnrange, tqdm_notebook
from nltk import word_tokenize

start = time.time()

file_eng = codecs.open("train.en", "r", "utf-8")
file_hin = codecs.open("train.hi", "r", "utf-8")

bitext = list()
count = 1

num_sentences = 40000

i = 0
pbar = tqdm(total = num_sentences)
while i<num_sentences:
    sent1 = tuple(word_tokenize(file_hin.readline().strip("\n")))
    sent2 = tuple(word_tokenize(file_eng.readline().strip("\n")))
    list_temp_hin = []
    list_temp_eng = []
    for word_hin in sent1:
        list_temp_hin.append(word_hin)
    for word_eng in sent2:
        list_temp_eng.append(word_eng)
    
    i+=1
    bitext.append([list_temp_eng, list_temp_hin])
    pbar.update(1)
pbar.close()
    # print(sen1)

e_count = defaultdict(float)
revf_count = defaultdict(float)
t_ef = defaultdict(float)   
t_fe = defaultdict(float)
align = defaultdict(float)
align_fe = defaultdict(float)
res_ef= []
res_fe= []

/ई__n_f
कला/ई__n_f


# print(bitext)
# print(bitext[1])
sys.stderr.write("initialization\n")
for (f, e) in bitext:
  le=len(e)
  lf=len(f)
  for (j, e_j) in enumerate(e):
      for (i, f_i) in enumerate(f):
        #t_ef[(e_j,f_i)] = 1.0/e_sz      ##check if uniform or to be carried over from ibm1
        align[(i,j,le,lf)] = 1.0/(lf) ##+1)
        align_fe[(j,i,le,lf)] = 1.0/(le)
#Get initial transition probabilities form ibm1- 5 iterations
ibm1_trans = open('ibm1')
t_ef = eval(ibm1_trans.readline())
for (e_j,f_i) in t_ef.keys():
    t_fe[(f_i,e_j)]=t_ef[(e_j,f_i)]
#sys.stderr.write(t_ef)

sys.stderr.write("starting EM\n")
index=0
while(index<16):    ##NOT CONVERGED
    index+=1
    sys.stderr.write(str(index))
    sys.stderr.write("\n")
    count_ef=defaultdict(float)   #automatically initialized to 0 for each e,f
    f_count = defaultdict(float)  #automatically initialized to 0
    count_a = defaultdict(float)  #automatically init to 0 for each i,j,le,lf
    total_a = defaultdict(float)  #automatically init to 0 for each i,j,le,lf
    count_fe = defaultdict(float)
    reve_count = defaultdict(float)
    count_rev_a = defaultdict(float)
    total_rev_a = defaultdict(float)
    for (n, (f, e)) in enumerate(bitext):
      le=len(e)
      lf=len(f)
      for (j,e_j) in enumerate(e):
          e_count[e_j] = 0
          for (i,f_i) in enumerate(f):      #What about null?
              e_count[e_j] += t_ef[(e_j,f_i)]*align[(i,j,le,lf)]

          for (i,f_i) in enumerate(f):
              temp = t_ef[(e_j,f_i)]*align[(i,j,le,lf)]/e_count[e_j]
              count_ef[(e_j,f_i)] += temp
              f_count[f_i] +=  temp
              count_a[(i,j,le,lf)] += temp
              total_a[(j,le,lf)] += temp
      for (i,f_i) in enumerate(f):
          revf_count[f_i] = 0
          for (j,e_j) in enumerate(e):      #What about null?
              revf_count[f_i] += t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)]

          for (j,e_j) in enumerate(e):
              temp = t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)]/revf_count[f_i]
              count_fe[(f_i,e_j)] += temp
              reve_count[e_j] +=  temp
              count_rev_a[(j,i,le,lf)] += temp
              total_rev_a[(i,le,lf)] += temp

    for (f, e) in bitext:
        le = len(e)
        lf = len(f)
        for (j, e_j) in enumerate(e):
            for (i, f_i) in enumerate(f):
                t_ef[(e_j,f_i)] = count_ef[(e_j,f_i)]/f_count[f_i]
                align[(i,j,le,lf)] = count_a[(i,j,le,lf)]/total_a[(j,le,lf)]

for (n,(f, e)) in enumerate(bitext):
  res_fe.append(set())
  for (i, f_i) in enumerate(f):
    best_prob = 0
    best_j=0
    for (j, e_j) in enumerate(e):
      if (t_ef[(e_j,f_i)]*align[(i,j,le,lf)])> best_prob:
        best_prob = t_ef[(e_j,f_i)]*align[(i,j,le,lf)]
        best_j  = j
      if (t_ef[(e_j,f_i)]*align[(i,j,le,lf)])== best_prob:
        if(abs(i-j)<abs(i-best_j)):
            best_prob = t_ef[(e_j,f_i)]*align[(i,j,le,lf)]
            best_j  = j
    res_fe[n].add((i,best_j))

for (n,(f, e)) in enumerate(bitext):
  res_ef.append(set())
  for (j, e_j) in enumerate(e):
      best_prob = 0
      best_i=0
      for (i, f_i) in enumerate(f):
         if(t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)]) > best_prob:
            best_prob = (t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)])
            best_i  = i
         if (t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)]) == best_prob:
            if(abs(j-i)<abs(j-best_i)):
                best_prob = t_fe[(f_i,e_j)]*align_fe[(j,i,le,lf)]
                best_i  = i
      res_ef[n].add((best_i,j))

for n in range(len(res_ef)):
    for (i,j) in res_ef[n]:
        #print (i,j)
        if((i,j) in res_fe[n]):
            sys.stdout.write("%i-%i " % (i,j))
    sys.stdout.write("\n")
