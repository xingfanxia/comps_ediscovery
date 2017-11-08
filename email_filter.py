import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

stop_Words = text.ENGLISH_STOP_WORDS

df = pd.read_csv("./data/parsed/training.csv")

import re

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
    ret = re.sub(replies, "", ret)
    return ret

'''
Method combining all filter methods
'''
def full_filter_email(df):
    df["Subject"] = df["Subject"].to_string(na_rep='')
    df["Subject"] = df["X-Cc"].to_string(na_rep='')
    df["Subject"] = df["X-Bcc"].to_string(na_rep='')
    print("SUBJECT CHANGE COMPLETED")
    df.loc[df["Subject"].str.lower().startswith('re')]["Message-Contents"].apply(filter_reply)
    print("REPLY FILTER COMPLETED")
    df["Message-Contents"] = df["Message-Contents"].apply(filter_email)
    print("EMAIL FILTER COMPLETED")

    return(df)

gross_email_filtered = pd.DataFrame()
gross_email_filtered = full_filter_email(df)
gross_email_filtered.to_pickle("filtered_email.pickle")
