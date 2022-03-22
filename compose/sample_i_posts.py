
import random, json

from tqdm import tqdm
from termcolor import colored
from collections import defaultdict
import os
import regex as re

DATA_DIR = '../data/2009/'
CUTOFF = 1000
FILE_TO_USE = 'RC_2009-01'

def main():
    get_sample()
    annotate_sample()

def annotate_sample():
    out = open('../samples/sample_i_am_a_annotated_sample', 'w')
    tallies = defaultdict(lambda: 0)
    i = 0
    try:
        with open('../samples/sample_i_am_a_sample') as handle:
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

def get_sample():
    i_am = []
    i_am_a = []
    as_a = []

    as_a_pattern = re.compile('as (a|an)', re.IGNORECASE)
    i_am_pattern = re.compile('((I am|I\'m))',re.IGNORECASE )
    i_am_a_pattern = re.compile('((I am|I\'m) *(also)* *(a|an))',re.IGNORECASE )
    # print(os.listdir())
    with open(DATA_DIR + FILE_TO_USE) as handle:
        lines = handle.readlines()
        # print(lines)
        for line in tqdm(lines):
            tline = json.loads(line)
            body = tline['body'].replace('\n', ' ').replace('\r', '').lower()

            if bool(re.search(i_am_pattern, body)):
                i_am.append(body)

            if bool(re.search(i_am_a_pattern, body)):
                i_am_a.append(body)
            if bool(re.search(as_a_pattern, body)):
                as_a.append(body)

    random.shuffle(i_am)
    random.shuffle(i_am_a)
    random.shuffle(as_a)

    with open('../samples/sample_i_am', 'w') as handle:
        for line in i_am[:CUTOFF]:
            handle.write(line + '\n')

    with open('../samples/sample_i_am_a', 'w') as handle:
        for line in i_am_a[:CUTOFF]:
            handle.write(line + '\n')

    with open('../samples/sample_as_a', 'w') as handle:
        for line in as_a[:CUTOFF]:
            handle.write(line + '\n')
if __name__ == '__main__':
    main()
