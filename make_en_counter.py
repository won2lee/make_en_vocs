# from "/Notebook/preProject/enko_new_bpe_vocabs_0616.ipynb"

import pandas as pd
from tqdm.notebook import tqdm
from itertools import chain
from collections import Counter
from util_func import json_read, json_save
import re

p1 = re.compile(r'[^A-Za-z0-9\'\-\.]')
q1 =re.compile(r'\.\s*$')
q2 = re.compile(r"\'\s")
q3 = re.compile(r"\s\'")
q4 = re.compile(r'\s+')

p_list = [p1,q1,q2,q3,q4]

en_chars = []
ko_words = []

path = "" #/home/john/Notebook/"
path2 = "out/" #preProject/create_vocabs_en/data/"

def modify_sent(sent,p_list):
    for p in p_list:
        sent = p.sub(' ',sent)
    return sent.strip()

def word_count(in_data, out_counts):
    
    for i in range(1000):
        if i*1000>len(in_data):break
        #en_ct = Counter()
        en_ct = Counter(chain(*[[w for w in modify_sent(s,p_list).split(' ')] for s in in_data[1000*i:1000*i+1000]]))
        out_counts += en_ct
    return out_counts

def count_en(to_count):
    
    en_wk = Counter()
    if 1 in to_count:
        print('start reading wiki_files')
        for ik in tqdm(range(160)):
            with open(path+"wiE/wiki_en"+str(ik)+".txt",'r') as f:
                X = f.read().split('\n')    
            en_wk = word_count(X, en_wk)     
        print("len(en_wk) :{}".format(len(en_wk)))
        json_save(en_wk,path+path2+'counted_vocs_en_wk')
    
    en_news = Counter()
    if 2 in to_count:
        print('start reading en_news_files')      
        for i in tqdm(range(1,4)):
            df = pd.read_csv(path+'newsEn/articles'+str(i)+'.csv') 
            en_news = word_count(df['content'], en_news)
        print("len(en_news) :{}".format(len(en_news)))
        json_save(en_news,path+path2+'counted_vocs_en_news')
    
    en_count = Counter()
    if 3 in to_count:
        print('start reading translated_ko_news_files')        
        for i in tqdm(range(1,5)):
            df = pd.read_excel(path+'newsKo/3_문어체_뉴스('+str(i)+')_191213.xlsx')
            parallel = df['ID 원문 번역문'.split(' ')]
            en_count = word_count(parallel['번역문'], en_count)
        print("len(en_count) :{}".format(len(en_count)))  
        json_save(en_count,path+path2+'counted_vocs_ko_news')

    json_save(en_count+en_news+en_wk,path+path2+'counted_vocs')

if __name__ == '__main__':
    to_count = [1,2,3]
    count_en(to_count)
