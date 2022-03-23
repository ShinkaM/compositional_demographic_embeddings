
import random, json

from tqdm import tqdm
from termcolor import colored
from collections import defaultdict
import os
import regex as re
from argparse import ArgumentParser




def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--dir', help='Dirctory where data is located', type=str)
    parser.add_argument('-f', '--file', help='File to sample i am post', type=str)
    parser.add_argument('-c', '--cutoff', help='max number of i am files to sample', default = 1000, type=int)
    opt = parser.parse_args()
    print(os.getcwd())
    DATA_DIR = opt.dir
    CUTOFF = opt.cutoff
    FILE_TO_USE = opt.file
    get_sample(DATA_DIR, FILE_TO_USE, CUTOFF)
    annotate_sample()

def annotate_sample():
    out = open('../samples/i_sample', 'w')
    tallies = defaultdict(lambda: 0)
    i = 0
    try:
        with open('../samples/sample_i_am_a') as handle:
            for line in handle.readlines():
                tline = line.strip().replace('\r', '')
                print(tline.replace('i am a', colored('i am a', 'red')).replace('i\'m a', colored('i\'m a', 'red')))
                x = input('Annotation (' + str(i) + '): ').strip()
                out.write(x + '\n')
                tallies[x] += 1
                i += 1
    except:
        print('Closing annotator...')
        for k,v in tallies.items():
            print(k + ': ' + str(v))

def get_sample(DATA_DIR, FILE_TO_USE, CUTOFF):
    # i_am = []
    i_am_a = []
    as_a = []
    mf = []

    # i_am_pattern = re.compile('^((I am|I\'m))[\w\s]+[?.!]$',re.IGNORECASE )
    i_am_a_pattern = re.compile('^((I am|I\'m) *(also)* *(a|an))[\w\s]+[?.!]$',re.IGNORECASE )
    as_a_pattern = re.compile('^as (a|an) [\w\s]+[?.!]$', re.IGNORECASE)
    mf_pattern = re.compile('^[\w\s]+[\[|\(]([0-9][0-9](f|F|m|M)|(f|F|m|M)[0-9][0-9])[\]|\)][\w\s]+[?.!]$', re.IGNORECASE)

    # print(os.listdir())
    with open(DATA_DIR + '/' + FILE_TO_USE) as handle:
        lines = handle.readlines()
        # print(lines)
        for line in tqdm(lines):
            print(line)
            tline = json.loads(line)
            body = tline['body'].replace('\n', ' ').replace('\r', '').lower()

            # if bool(re.search(i_am_pattern, body)):
            #     i_am.append(body)

            if bool(re.search(i_am_a_pattern, body)):
                i_am_a.append(body)
            if bool(re.search(as_a_pattern, body)):
                as_a.append(body)
            if bool(re.search(mf_pattern, body)):
                mf.append(body)

    random.shuffle(mf)
    random.shuffle(i_am_a)
    random.shuffle(as_a)

    # with open('../samples/sample_i_am', 'w') as handle:
    #     for line in i_am[:CUTOFF]:
    #         handle.write(line + '\n')
    with open('../samples/sample_mf', 'w') as handle:
        for line in mf[:CUTOFF]:
            handle.write(line + '\n')

    with open('../samples/sample_i_am_a', 'w') as handle:
        for line in i_am_a[:CUTOFF]:
            handle.write(line + '\n')

    with open('../samples/sample_as_a', 'w') as handle:
        for line in as_a[:CUTOFF]:
            handle.write(line + '\n')
if __name__ == '__main__':
    main()
