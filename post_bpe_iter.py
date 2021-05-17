
#####################################

#   6.15 version

#####################################

import re
import copy
import pandas as pd
from tqdm.notebook import tqdm
from itertools import chain
from collections import Counter
from util_func import json_read, json_save, dict_merge, voc_combined, add_item, modi_dict

def bpe_voc_in_normal(bpe_vocabs):
    voc_ex, _ = voc_combined(bpe_vocabs)
    sorted_voc_ex = sorted(voc_ex.items(), key=lambda x:x[1], reverse=True)
    #readable = [(special_to_normal(k,key_vars),v) for k, v in sorted_voc_ex]
    return sorted_voc_ex
    #return readable, sorted_voc_ex


def main():
    path = "data/"

    new_bpe_vocabs = json_read(path+'bpe_iter/vocabs10000.json')
    after_bpe = bpe_voc_in_normal(new_bpe_vocabs)
    Xstart = dict(after_bpe)
    #XX = copy.deepcopy(Xstart)

    vocabs = json_read(path+'counted_vocs.json')
    Xvocs = {}
    for w,v in vocabs.items():
        add_item(w.lower(),v,Xvocs)
    vocabs = copy.deepcopy(Xvocs) 
    to_save = ['bpe30', 'count30']

    for ik,vcs_set in enumerate([Xstart, vocabs]):
        XX = copy.deepcopy(vcs_set)
        XXX = copy.deepcopy(XX)
        print("step_1 XX : {}".format(len(XX)))
        print('success' in XX.keys())

        Xa = {}
        for k,v in XX.items():
            if (len(k) >3 and k[-1] =='.' and (k[:-1] in vocabs.keys())):
                modi_dict(k,1,v,Xa,XXX)

        _,_ = dict_merge(Xa,XXX)
        XX = copy.deepcopy(XXX)
        print("step_2 XX : {}".format(len(XX)))
        print('success' in XX.keys())

        Xa = {}
        for k,v in XX.items():
            if (len(k) > 6 and k[-1] =="s" and k[-2:] not in ["es","ss"] and 
                k in vocabs.keys() and k[:-1] in vocabs.keys()) and vocabs[k[:-1]] > 0.2 * vocabs[k]:
                modi_dict(k,1,v,Xa,XXX)

        _,_ = dict_merge(Xa,XXX)
        XX = copy.deepcopy(XXX)
        print("step_3 XX : {}".format(len(XX)))
        print('success' in XX.keys())

        Xa = {}
        for k,v in XX.items():
            if (len(k) > 6 and k[-2:] =='ly' and 
                k in vocabs.keys() and k[:-2] in vocabs.keys() and vocabs[k[:-2]] > 0.2 * vocabs[k]):
                modi_dict(k,2,v,Xa,XXX)

        _,_ = dict_merge(Xa,XXX)
        XX = copy.deepcopy(XXX)
        print("step_4 XX : {}".format(len(XX)))

        Xa = {}
        for k,v in XX.items():
            if (len(k) >7 and k[-4:] in ['ness','ment'] and 
                k in vocabs.keys() and k[:-4] in vocabs.keys() and vocabs[k[:-4]] > 0.2 * vocabs[k]):
                modi_dict(k,4,v,Xa,XXX)

        _,_ = dict_merge(Xa,XXX)
        XX = copy.deepcopy(XXX)
        print("step_5 XX : {}".format(len(XX))) 
        print('success' in XX.keys())

        for k,v in XX.items():

            if (len(k) > 8 and k[-5:] =='ation' and k in vocabs.keys() and k[:-5]+'ed' in vocabs.keys() and 
                ((k[:-5] in vocabs.keys() and vocabs[k[:-5]] > 0.2 * vocabs[k]) or 
                 (k[:-5]+'e' in vocabs.keys() and vocabs[k[:-5]+'e'] > 0.2 * vocabs[k]))):
                modi_dict(k,5,v,Xa,XXX)

            elif (len(k) > 6 and k[-3:] in ['ion', 'ing'] and k in vocabs.keys() and k[:-3]+'ed' in vocabs.keys() and
                  ((k[-5] == k[-4] and k[:-3] in vocabs.keys() and k[:-4] not in vocabs.keys()) or 
                   (k[-5] != k[-4] and ((k[:-3] in vocabs.keys() and vocabs[k[:-3]] > 0.2 * vocabs[k]) 
                        or (k[:-3]+'e' in vocabs.keys() and vocabs[k[:-3]+'e'] > 0.2 * vocabs[k]))))): # discuss 와 같은 경우 
                modi_dict(k,3,v,Xa,XXX)

            elif (len(k) > 5 and k[-2:] in ['ed','es','er'] and 
                  ((k[-3] == k[-4] and k[:-2] in vocabs.keys() and k[:-3] not in vocabs.keys()) or 
                   (k[-3] != k[-4] and (k[:-2] in vocabs.keys() or k[:-2]+'e' in vocabs.keys()))) and 
                  k in vocabs.keys() and k[:-2]+'ing' in vocabs.keys()):
                modi_dict(k,2,v,Xa,XXX)

            elif (len(k) > 4 and k[-2:] == "'s" and k[:-2] in vocabs.keys()):
                modi_dict(k,2,v,Xa,XXX)

            elif (len(k) > 4 and k[-1:] in ["s"] and k[-2:] not in ["es","ss"] and k in vocabs.keys() and 
                  k[:-1] in vocabs.keys() and vocabs[k[:-1]] > 0.3*vocabs[k]):
                modi_dict(k,1,v,Xa,XXX)

            elif (len(k) > 4 and k[-1:] in ["e"] and k in vocabs.keys() and 
                  k[:-1]+'ing' in vocabs.keys() and k[:-1]+'ed' in vocabs.keys() and 
                  vocabs[k] < vocabs[k[:-1]+'ing'] + vocabs[k[:-1]+'ed']):
                modi_dict(k,1,v,Xa,XXX)

        _,_ = dict_merge(Xa,XXX)        
        XX = copy.deepcopy(XXX) 
        print("step_6 XX : {}".format(len(XX)))
        print('success' in XX.keys())

        p = re.compile('.*[0-9]+.*')
        for k,v in XX.items():
            if p.sub('',k) =='':
                XXX.pop(k,1) 
        XX = copy.deepcopy(XXX) 
        print("step_7 XX : {}".format(len(XX)))


        if ik == 1:
            XX = dict(sorted(XX.items(), key=lambda x:x[1],reverse=True)[:30000])
        json_save(XX,path+'en_vocabs/'+to_save[ik]+'_0615_check')

    vocsX = json_read(path+'en_vocabs/count30_0615.json')
    X30000 = json_read(path+'en_vocabs/bpe30_0615.json')
    print(len(vocsX), len(X30000))
    _,_ = dict_merge(X30000,vocsX)
    Xffix = json_read(path+'en_vocabs/pre_suf_fix.json')
    print(len(vocsX), len(Xffix['prefix']))
    vocsX.update(Xffix['prefix'])
    vocsX.update(Xffix['suffix'])
    print(len(vocsX), len(Xffix['prefix']))
    json_save(vocsX,path+'en_vocabs/en_vocabs_to_apply.json')

if __name__ == __main__:
    main()
