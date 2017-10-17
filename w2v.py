
# coding: utf-8

# ## Data Preparation



import pandas as pd



df = pd.read_csv("data/emails.csv")


# ## Match ID


import csv, sys, os, re


def list_files(dir):
    r = []
    for f in os.listdir(dir):
        if re.match(r'3\.[0-9]*\.[A-Z0-9]*\.txt', f):
            r.append(f)
    return r


def is_empty_email(contents):
    empty_pattern = re.compile("X-ZLID:.*(\r|\n)*\*{11}[\r\n]EDRM Enron Email", re.MULTILINE)
    if empty_pattern.search(contents):
         return True
    return False

def match_trec(file):
#     to_pattern = r"To:.*<(.*)>"
    from_pattern = r"From:(.*)"
    contents_pattern = re.compile("X-ZLID:.*[\r\n]((?:.|\r|\n)*)\*{11}[\r\n]EDRM Enron Email", re.MULTILINE)
    from_name = file.split('/')[-3][14:-8]
    date_pattern = r"Date: (.*)"
    with open(file, 'r') as text:
        string = text.read()
        if not is_empty_email(string):
            try:
    #             to_string = re.search(to_pattern, string).group(1)
#                 from_string = re.search(from_pattern, string).group(1)
                contents = re.search(contents_pattern, string).group(1).replace('\n','').strip()
                date_string = re.search(date_pattern, string).group(1)
                return (from_name, date_string, contents)
            except:
                print(file)
                print(string)



file_list = list_files('data/trecdata/text_000/')

trecid2info = dict()
text2trecid = dict()
for f in file_list:
    trecid = f[:-4]
    info = match_trec('data/trecdata/text_000/' + f)
    if info:
        trecid2info[trecid] = info
        text = info[2]
        if text in text2trecid.keys():
            text2trecid[text].append(trecid)
        else:
            text2trecid[text] = [trecid]


#parse qrels file
ids = pd.read_csv('data/qrels.txt', sep=r'\s', header=None, names=['id', 'stratum', 'label'])

def extract_scenario(string):
    return string[:3]

def clean_id(string):
    return string[4:]


ids['scenario'] = ids.id.apply(extract_scenario)

ids['id'] = ids.id.apply(clean_id)

relevant = [x for x in ids if x['label'] == '1']
irrelevant = [x for x in ids if x['label'] == '0']
print('Relevant',relevant)

#given a message from .csv, get the message
def get_contents(message):
    contents_pattern = re.compile("X-FileName.*([\s\S]*)", re.MULTILINE)
    contents = re.search(contents_pattern, message).group(1).replace('\n','').strip()
    return contents

import difflib

found_cnt = 0.0
unclear_cnt = 0

for message in df['message']:
    contents = get_contents(message)
    try:
        matches = text2trecid[contents]
    except KeyError:
        print('No matches found')
        unclear_cnt += 1
    if len(matches) > 1:
        #fancy stuff here
        print(text2trecid[matches])
        unclear_cnt += 1
    else:
        print(text2trecid[matches[0]])
        found_cnt += 1
print('Percent correct: {}'.format(float(found_cnt)/(found_cnt+unclear_cnt)))