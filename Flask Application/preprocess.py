import os 
import time
from pymongo import MongoClient
from fetch_data import fetch_all_data
import re
import numpy as np
from random import randint as rint
from tqdm import tqdm

def preProcessData(data,fg = False):
    ndata = []
    ln = 0
    for doc in tqdm(data):
        if fg:
            doc,_ = doc
        doc = doc.lower()
        doc = doc.replace('\n'," ")
        doc = re.sub('[\W_]+', ' ', doc)
        if not fg:
          ndata.append(doc.split()[:250] + [doc[rint(0,len(doc)-1)] for _ in range(250)] + doc.split()[-250:])
        else:
          ndata.append(doc.split())      
    return ndata


def shingleText(text,shingleSize = 3):
    shingles = []
    for i in tqdm(range(len(text)-shingleSize+1)):
        if i + shingleSize < len(text):
            shingles.append(" ".join(text[i:i+shingleSize]))
    return shingles


def convertToFreq(data):
    wrds,iwcnt = dict(),1
    shingles_docs = []
    rfeatures = list()
    for doc in tqdm(data):
        shingles = shingleText(doc)
        #print(shingles)
        for wrd in shingles:
            if wrds.get(wrd,0) == 0:
                wrds[wrd] = iwcnt
                iwcnt += 1
        shingles_docs.append(shingles)
    
    ndocs = []

    for sdoc in tqdm(shingles_docs):
        tli = dict()
        for swrd in sdoc:
            tli[wrds[swrd]-1] =  tli.get(wrds[swrd]-1,0) + 1
        if len(sdoc):
            rfeatures.append(wrds[sdoc[0]]-1)
        ndocs.append(tli)
    return ndocs,wrds,set(rfeatures)
