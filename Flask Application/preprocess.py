import os
import re
import time
from random import randint as rint

import numpy as np
from fetch_data import fetch_all_data
from pymongo import MongoClient
from tqdm import tqdm


def preProcessData(data,fg = False):
    ndata = []
    ln = 0
    for doc in data:
        if fg:
            doc,_ = doc
        doc = doc.lower()
        doc = doc.replace('\n'," ")
        
        doc = re.sub('[\W_]+', ' ', doc)
        if fg:
            ndata.append(doc.split()[:250] + [doc[rint(0,len(doc)-1)] for _ in range(250)] + doc.split()[-250:])
        else:
            ndata.append(doc.split())      
    return ndata

def shingleText(text,shingleSize = 3):
    shingles = []
    for i in range(len(text)-shingleSize+1):
        if i + shingleSize < len(text):
            shingles.append(" ".join(text[i:i+shingleSize]))
    return shingles

def convertToFreq(data):
    wrds,iwcnt = dict(),1
    shingles_docs = []
    rfeatures = list()
    for doc in data:
        shingles = shingleText(doc)
        #print(shingles)
        for wrd in shingles:
            if wrds.get(wrd,0) == 0:
                wrds[wrd] = iwcnt
                iwcnt += 1
        shingles_docs.append(shingles)
    
    ndocs = []
    for sdoc in shingles_docs:
        tli = dict()
        for swrd in sdoc:
            tli[wrds[swrd]-1] =  tli.get(wrds[swrd]-1,0) + 1
        if len(sdoc):
            rfeatures.append(wrds[sdoc[0]]-1)
            for _ in range(2):
                rfeatures.append(wrds[sdoc[rint(0,len(sdoc)-1)]]-1)
        ndocs.append(tli)
    del shingles_docs
    return ndocs,wrds,set(rfeatures)

