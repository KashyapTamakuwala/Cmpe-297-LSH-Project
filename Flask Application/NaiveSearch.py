import time 
import numpy as np
from numpy.linalg import norm
from preprocess import shingleText, preProcessData

def naiveSimDocs(data,qd,wrds, k =5):
    sim_func = lambda x,y:  x.dot(y.T)/((norm(x)*norm(y))+1e-4)
    num_ts,num_tr = len(qd),len(data)

    nbrs = np.zeros((num_ts,k),dtype=np.int32)
    nvals = np.zeros((num_ts,k),dtype=np.double)

    qpre_data = [shingleText(row) for row in preProcessData(qd)]
    queries = []
    for sdoc in qpre_data:
        tli = dict()
        for swrd in sdoc:
            if wrds.get(swrd,0):
                tli[wrds[swrd]-1] = tli.get(wrds[swrd]-1,0) + 1
        queries.append(tli)
    for i in range(num_ts):
        #simd = [sim_func(qd[i],data[j]) for j in range(num_tr)]
        arr1 = np.asarray([0]*len(wrds))
        qD = queries[i]
        for key in qD:
            arr1[key] += qD[key]
        simd = []
        for j in range(10):
            arr2 = np.asarray([0]*len(wrds))
            np.put(arr2,list(data[j].keys()),list(data[j].values()))
            simd.append(sim_func(arr1,arr2))
        prob = np.argsort(simd)
        nbrs[i,:] = prob[:k]
        nvals[i,:] = [simd[k] for j in prob[:k]]
    return nbrs,nvals

def recall(predicted,true_nbr):
    acc = 0.0
    n,k = true_nbr.shape
    for i in range(n):
        x,y = predicted[i,:],true_nbr[i,:]
        acc += np.interesect1d(x,y).shape[0]/float(k)
    return acc/float(n)