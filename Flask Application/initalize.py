from LSH import LSH
from preprocess import convertToFreq,preProcessData
from fetch_data import fetch_all_data
import traceback
import logging

def initalize(data):    
    print("started initalization")
    try:
        ## Preporcessing data
        print("Preprocessing data")
        pdata = preProcessData(data,True)
        print("Frequency counter")
        fdata,wrds,red_features = convertToFreq(pdata)
        print("Initalizing LSH")
        l1 = LSH(fdata,wrds,10,10,10000,red_features=red_features)
    except Exception as ex:
        logging.error(traceback.format_exc())
    print("Complete initalization")
    return l1