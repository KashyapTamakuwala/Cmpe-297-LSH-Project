from pymongo import MongoClient
import os
import time
from alive_progress import alive_bar

def fetch_all_data():
    data_list=[]
    mongoclinet= MongoClient("mongodb+srv://Kashyap:<password>@cmpe-297-project.hyaud2z.mongodb.net/?retryWrites=true&w=majority")
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