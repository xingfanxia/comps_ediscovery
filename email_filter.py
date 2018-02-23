import numpy as np
import pandas as pd
import re

from datetime import datetime
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer


'''
Email filter class that will hold all of our regexes that we can apply to ALL emails. It is helpful
to have it as an objectbecause we can just add the regexes as instance variables and then iterate
over all of them using <object>.__dict__.items()
'''
class Email_filter:
     def __init__(self):
        ##regexes#
        self.quoted = re.compile(r"^>(\s)*", re.MULTILINE)
        self.original_or_forward = re.compile(r"(^(\s)*-*(\s)*Original Message(\s)*-.*$)|(^____.*$)", re.MULTILINE)
        self.metadata = re.compile(r"(^From:.*$)|(^Sent:.*$)|(^To:.*$)|(^Subject:.*$)|(^Cc:.*$)|(^Date:.*$)|(^Encoding:.*$)", re.MULTILINE)
        self.ole_object = re.compile(r"(<<.*?>>)+", re.DOTALL|re.MULTILINE)
        self.smtp_header = re.compile(r"^Message-id:.*?X-Mozilla-Status.*?$", re.DOTALL|re.MULTILINE)
        self.received = re.compile(r"^Received:(.*?)\([A-Z]{3}\)", re.DOTALL|re.MULTILINE)

'''
Method to actually filter the emails - creates an email filter object and loops through all of the
regexes it contains, running each of them on an email. If the email is a reply, it will first
cut out all of the replies.
'''
def filter_email(s):
    if type(s) != str:
        return("")
    e = Email_filter()
    ret = s
    for variable_name, regex in e.__dict__.items():
        ret = re.sub(regex, "", ret)

    return ret

'''
Method to cut out all of the replies of emails
'''
def filter_reply(s):
    replies = re.compile(r"(^(\s)*-*(\s)*Original Message.*)", re.MULTILINE|re.DOTALL)
    ret = re.sub(replies, "", s)
    return ret


'''
metadata parsing
'''
def parse_date(d):
    d = d.replace(',', '')
    redundancy_filter = d.split(' (')
    string = redundancy_filter[0]
    datetime_object = datetime.strptime(string, '%a %d %b %Y %X %z')
    return datetime_object


def x_strip(s):
    if s != "":
        array = re.split(r'</O.*?\>', s)
        array = [x.strip() for x in array]
        return array
    else:
        return([])

def to_from_strip(s):
    if s != "":
        return s.split(',')
    else:
        return([])

def parse_metadata(df):
    df['Date'] = df['Date'].apply(parse_date)
    df['To'] = df['To'].apply(to_from_strip)
    df['From'] = df['From'].apply(to_from_strip)
    df['X-To'] = df['X-To'].apply(x_strip)
    df['X-From'] = df['X-From'].apply(x_strip)
    return(df)

def full_filter_email(df):
    df = df.replace(np.nan, '', regex=True)
    df.loc[df["Subject"].str.lower().str.startswith('re')]["Message-Contents"].apply(filter_reply)
    df["Message-Contents"] = df["Message-Contents"].apply(filter_email)
    df = parse_metadata(df)
    return(df)



#'''
#Email filter class that will hold all of our regexes that we can apply to ALL emails. It is helpful
#to have it as an objectbecause we can just add the regexes as instance variables and then iterate
#over all of them using <object>.__dict__.items()
#'''
#class Email_filter:
#     def __init__(self):
#        ##regexes#
#        self.quoted = re.compile(r"^>(\s)*", re.MULTILINE)
#        self.original_or_forward = re.compile(r"(^(\s)*-*(\s)*Original Message(\s)*-.*$)|(^____.*$)", re.MULTILINE)
#        self.metadata = re.compile(r"(^From:.*$)|(^Sent:.*$)|(^To:.*$)|(^Subject:.*$)|(^Cc:.*$)|(^Date:.*$)|(^Encoding:.*$)", re.MULTILINE)
#        self.ole_object = re.compile(r"(<<.*?>>)+", re.DOTALL|re.MULTILINE)
#        self.smtp_header = re.compile(r"^Message-id:.*?X-Mozilla-Status.*?$", re.DOTALL|re.MULTILINE)
#        self.received = re.compile(r"^Received:(.*?)\([A-Z]{3}\)", re.DOTALL|re.MULTILINE)
#
#'''
#Method to actually filter the emails - creates an email filter object and loops through all of the
#regexes it contains, running each of them on an email. If the email is a reply, it will first
#cut out all of the replies.
#'''
#def filter_email(s):
#    if type(s) != str:
#        return("")
#    e = Email_filter()
#    ret = s
#    for variable_name, regex in e.__dict__.items():
#        ret = re.sub(regex, "", ret)
#
#    return ret
#
#'''
#Method to cut out all of the replies of emails
#'''
#def filter_reply(s):
#    replies = re.compile(r"(^(\s)*-*(\s)*Original Message.*)", re.MULTILINE|re.DOTALL)
#    ret = re.sub(replies, "", ret)
#    return ret
#
#'''
#Method combining all filter methods
#'''
#def full_filter_email(df):
#    df["Subject"] = df["Subject"].to_string(na_rep='')
#    df["Subject"] = df["X-Cc"].to_string(na_rep='')
#    df["Subject"] = df["X-Bcc"].to_string(na_rep='')
#    print("SUBJECT CHANGE COMPLETED")
#    df.loc[df["Subject"].str.lower().startswith('re')]["Message-Contents"].apply(filter_reply)
#    print("REPLY FILTER COMPLETED")
#    df["Message-Contents"] = df["Message-Contents"].apply(filter_email)
#    print("EMAIL FILTER COMPLETED")
#
#    return(df)
