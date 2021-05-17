import re
import collections
from collections import Counter
from tqdm.notebook import tqdm

def json_save(data, f_name):
    import json
    json = json.dumps(data)
    with open(f_name +".json","w") as f:
        f.write(json) 

def json_read(f_name):
    import json
    with open(f_name) as f:
        return json.load(f)
    
def dict_merge(src_dict, tgt_dict):
    
    updated_items = 0
    added_items = 0
    
    for k,v in tqdm(src_dict.items()):
        if k in tgt_dict.keys():
            tgt_dict[k] =  tgt_dict[k] + v 
            updated_items += 1
        else:
            tgt_dict[k] = v
            added_items += 1
    
    print("updated items : {},  added items : {}".format(updated_items, added_items)) 
    
    return updated_items, added_items

def add_item(k,v,dct):
    if k in dct.keys():
        dct[k] += v
    else:
        dct[k] = v
        
def modi_dict(k,l,v,dt_to_add,dt_to_pop):
    add_item(k[:-l], v, dt_to_add)
    add_item(k[-l:], v, dt_to_add)
    dt_to_pop.pop(k,1)

def voc_combined(vocab):
    vocab_sub = {}
    #for k, v in vocab:
    for k, v in vocab.items():
        for s in k.split(' '): 
            if s in vocab_sub.keys():
                vocab_sub[s] += v
            else:
                vocab_sub[s] = v
    return vocab_sub, len(vocab_sub)

def bpe_vocab_iteration(path, iter_size,step_from_start, step_size = 250):

    save_cyc =1000

    vocabs =json_read(path+'vocabs' + str(step_from_start)+'.json')
    vocabs_freq =json_read(path+'vocs_freq' + str(step_from_start)+'.json')
    new_bpe_vocabs,vocabs_f,_,_ = vocab_select2(vocabs, vocabs_freq, path, iter_size, step_size, step_from_start, save_cyc)
    return new_bpe_vocabs, vocabs_f


def vocab_select2(vocabs,vocabs_freq, path,iter_size, step_size,step_from_start,save_cyc):
    pre_voc_volume = 0
    n = 0
    for i in tqdm(range(iter_size//step_size)):
        
        vocabs, vocabs_freq = dpe_iteration2(vocabs, vocabs_freq, step_size)
        _, voc_volume = voc_combined(vocabs) 
        print("iter_number :{}, voc_volume : {}".format((i+1)*step_size+step_from_start, voc_volume))
        iter_n = (i+1) * step_size 
        if iter_n % save_cyc == 0:
            json_save(vocabs, path+ 'vocabs' + str(step_from_start+iter_n))
            json_save(vocabs_freq, path+ 'vocs_freq'+str(step_from_start+iter_n))
           
        if voc_volume < pre_voc_volume:n+=1
        pre_voc_volume = voc_volume
        if n>3:break
       
    step_from_start += iter_size
    
    return vocabs, vocabs_freq, voc_volume, step_from_start


def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out
""" 
vocab = {'l o w </w>' : 5,
         'l o w e r </w>' : 2,
         'n e w e s t </w>':6,
         'w i d e s t </w>':3
         }
"""


def dpe_iteration2(vocab, vocabs_freq, iter_num):
    num_merges = iter_num
    new_best = []
    for i in tqdm(range(num_merges)):
        pairs = get_stats(vocab)
        #print(f'pairs : {pairs.get}')
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
        vocabs_freq[''.join(best)] = (best, pairs[best])
        new_best.append(best)
        if i%50 == 49:
            print([[q for q in p] for p in new_best])
            new_best = []
    return vocab, vocabs_freq    


