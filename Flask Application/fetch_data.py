from pymongo import MongoClient
import os
import time
from alive_progress import alive_bar
from tqdm import tqdm

def fetch_all_data():
    data_list=[]
    mongoclinet= MongoClient("mongodb+srv://Kashyap:Kt1234@cmpe-297-project.hyaud2z.mongodb.net/?retryWrites=true&w=majority")
    mydb = mongoclinet["Cmpe-297-database"]

    ## Collection
    mycol = mydb["Data"]
    cursor = mycol.find({})

    with alive_bar(13886) as bar:
        for document in cursor:
            data_list.append([document["document_data"],document["document_key"]])
            bar()
    mongoclinet.close()
    return data_list

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

def fetch_data_local():
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
            
    return data