from pymongo import MongoClient
import os 
from alive_progress import alive_bar
import numpy as np
from numpy import dot
from numpy.linalg import norm


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
    mongoclinet.close()
    return data_list


# dimension of A = (a*b) and b = (c*b)
def cosine_similarity(A,B):
    num=np.dot(A,B.T)
    p1=np.sqrt(np.sum(A**2,axis=1))[:,np.newaxis]
    p2=np.sqrt(np.sum(B**2,axis=1))[np.newaxis,:]
    return num/(p1*p2)
if __name__ == "__main__":
    #data=fetch_all_data()
    #print(data[0])
    print(cosine_similarity([1,1,1],[1,1,1]))