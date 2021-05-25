import copy
from tqdm.notebook import tqdm
from util_func import json_read, json_save, dict_merge, add_item, modi_dict
"""    
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
    
"""

def main(): 
    import copy   
    X = json_read('./data/counted_vocs.json')
    Vocabs = {k.strip():v for k,v in X.items() if v>2}
    Vocabs.pop('',1)
    Vocabs.pop('.',1)
    print("Vocabs ; {}".format(len(Vocabs)))
    
    ############################################???????
    sffx1 = 'd s r .'.split(' ')
    sffx2 = "es ed er 's".split(' ') 
    sffx3 = ["est", "ing"]

    vocabs = {}
    for k,v in Vocabs.items():
        add_item(k.lower(), v, vocabs)

    print("vocabs ; {}".format(len(vocabs)))

    de_dotted = {}
    XX = copy.deepcopy(vocabs)
    for k,v in tqdm(vocabs.items()):
        if (len(k) >3 and k[-1] =='.' and (k[:-1] in vocabs.keys())):  
            modi_dict(k,1,v,de_dotted,XX)

    _,_ = dict_merge(de_dotted,XX)
    vocabs = copy.deepcopy(XX)

    for k,v in tqdm(vocabs.items()):
        if (len(k) >6 and k[-4:] in ['ness','ment'] and k[:-4] in vocabs.keys()):
            modi_dict(k,4,v,de_dotted,XX)

    _,_ = dict_merge(de_dotted,XX)
    vocabs = copy.deepcopy(XX)

    for k,v in tqdm(vocabs.items()):

        if (len(k) >5 and k[-3:] in ['ing','ion'] and 
            (k[:-3] in vocabs.keys() or k[:-3]+'e' in vocabs.keys() or k[:-3]+'ed' in vocabs.keys())):
            modi_dict(k,3,v,de_dotted,XX)

        elif (len(k) > 4 and k[-2:] in ['er','es','ed'] and 
              (k[:-2]+'e' in vocabs.keys() or (k[:-2] in vocabs.keys() and vocabs[k] < vocabs[k[:-2]]*3)) 
               and k[:-2]+'ed' in vocabs.keys()):
            modi_dict(k,2,v,de_dotted,XX)

        elif len(k) >4 and k[-2:] in ["'s","ly"] and k[:-2] in vocabs.keys():
            modi_dict(k,2,v,de_dotted,XX)

        elif (len(k) >3 and k[-1] in ['s','e'] and (k[:-1]+'ed' in vocabs.keys() or k[:-1] in vocabs.keys())): 
            modi_dict(k,1,v,de_dotted,XX)

    print(len(de_dotted), len(vocabs), len(XX))
    #vocabs = {k:v for k,v in vocabs.items() if k[-1] !='.'}
    _,_ = dict_merge(de_dotted,XX)     

    print("de_dotted ; {}".format(len(de_dotted)))
    print("XX ; {}".format(len(XX)))

    path = "./data/en_vocabs/"
    pre_suffx = json_read('pre_suffx/pre_suffx_0515.json') 
    pre_fx = [k.capitalize() for k in pre_suffx["prefixes"]] + pre_suffx["prefixes"]
    suf_fx = pre_suffx["suffixes"]

    pre_fx = sorted(list(set(pre_fx)), key=lambda x:len(x), reverse = True)
    suf_fx = sorted(list(set(suf_fx)), key=lambda x:len(x), reverse = True)

    import copy
    #en_count = json_read('./en_es_after_0613/counted_vocs_0613.json')
    XXX = copy.deepcopy(XX)
    #c_chars = [chr(i) for i in range(ord('A'),ord('Z')+1)]

    prefx = {k:100 for k in pre_fx}
    suffx = {k:100 for k in suf_fx}

    p_multi = 0.2
    s_multi = 0.2

    for k,v in tqdm(XXX.items()):

        for s in [pf for pf in pre_fx if len(pf)<len(k)+1]:
            if k[:len(s)] == s:
                prefx[s] += int(v * len(s) * p_multi)
                break

        for s in [pf for pf in suf_fx if len(pf)<len(k)]:
            if k[-len(s):] == s:
                suffx[s] += int(v * len(s) * s_multi)
                break        

    pf = sorted(prefx.items(), key=lambda x:x[1], reverse = True)
    sf = sorted(suffx.items(), key=lambda x:x[1], reverse = True)

    print(pf[:20])
    print(sf[:20])

    path = "./data/en_vocabs/"
    Xffix ={'prefix':prefx,'suffix':suffx}
    json_save(Xffix,path+'pre_suf_fix')
    XXX.update(prefx)
    XXX.update(suffx)
    json_save(XXX,path+'counted_vocs_0613_added_pre_suffx')
    vocabs = {' '.join([c for c in k]):v for k,v in XXX.items()}
    json_save(XXX, path+'vocabs')

if __name__ == "__main__":
    main()
