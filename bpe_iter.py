
from util_func import json_read, json_save, bpe_vocab_iteration

path = 'data/bpe_iter/'

step_from_start = 7000
iter_size = 10000
step_size = 250

def main():

    if step_from_start == 0:
        vocabs = json_read('data/en_vocabs/vocabs.json')
        vocabs = {' '.join([c for c in k]):v for k,v in vocabs.items()}
        vocabs_freq = {}
        json_save(vocabs,path+'vocabs'+str(0))
        json_save(vocabs_freq,path+'vocs_freq'+str(0))

    new_bpe_vocabs, vocabs_freq =bpe_vocab_iteration(path, iter_size,step_from_start, step_size)

if __name__ == "__main__":
    main()
