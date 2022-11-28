from pymongo import MongoClient
import os 
from alive_progress import alive_bar


def fetch_all_data():
    data_list=[]
    mongoclinet= MongoClient("mongodb+srv://Kashyap:Kt1234@cmpe-297-project.so36aaq.mongodb.net/?retryWrites=true&w=majority")


    ## Creating Database
    mydb = mongoclinet["Cmpe-297-database"]

    ## Collection
    mycol = mydb["Data"]
    cursor = mycol.find({})
    with alive_bar(13355) as bar:
        for document in cursor:
            data_list.append([document["document_data"],document["document_key"]])
            bar()
    return data_list

if __name__ == "__main__":
    data=fetch_all_data()
    print(data[0])