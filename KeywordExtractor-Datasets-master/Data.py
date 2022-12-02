from pymongo import MongoClient
import os 
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm

def get_data(folder_path,file_list):
    data=[]
    for i in tqdm(file_list):
        ## document data
        f=open(folder_path+'/'+'docsutf8'+'/'+i,encoding='utf-8')
        temp_data=f.read()
        #print(temp_data)

        ##key_data
        key_file=i[0:-3]+'key'
        k=open(folder_path+'/'+'keys'+'/'+key_file,encoding='utf-8')
        temp_keys=k.readlines()
        #print(temp_keys)

        dict={'document_data': temp_data,'document_key':temp_keys}
        data.append(dict)
    return data

def get_file_list(folder_path):
    file_list=[]
    for i in os.listdir(folder_path+'/'+'docsutf8'):
        file_list.append(i)
    return file_list

def data_insert_mongo(data):

    mongoclinet= MongoClient("mongodb+srv://Kashyap:Kt1234@cmpe-297-project.hyaud2z.mongodb.net/?retryWrites=true&w=majority")


    ## Creating Database
    mydb = mongoclinet["Cmpe-297-database"]

    ## Collection
    mycol = mydb["Data"]

    ## Inserting data
    x = mycol.insert_many(data)
    mongoclinet.close()
    
    return x.inserted_ids

def merge_data(final_data,data):
    for i in data:
        final_data.append(i)
    return final_data

if __name__ == "__main__":
    path=r"C:/Users/s0349821/Desktop/College/code/KeywordExtractor-Datasets-master/datasets"
    final_data=[]
   
    folder_list=[]
    for i in os.listdir(path):
        folder_list.append(path+"/"+i)

    data=[]
    for f in folder_list:
        print(f)
        file_list=get_file_list(f)
        data_list=get_data(f,file_list)
        for i in data_list:
            data.append([i['document_data'],i['document_key']])
            
    print(len(data))
        #final_data=merge_data(final_data,data_list)
    


        