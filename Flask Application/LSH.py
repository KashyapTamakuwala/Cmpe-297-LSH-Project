import numpy as np
from numpy.linalg import norm
from preprocess import preProcessData,shingleText

class LSH:
    def __init__(self,data,features,nfunc,ntabs,nfeatures,red_features,rfeature_size = 10000):
        self.data = data
        self.features = features
        self.rdata = []
        self.rfeature_size = rfeature_size
        self.red_features = red_features
        self.rfeatures = None
        self.nfeatures = nfeatures
        self.nfunc = nfunc
        self.ntabs = ntabs
        
        self.hsh_fn_tb = [{} for _ in range(ntabs)]
        self.tables = [dict() for _ in range(ntabs)]
        self.randFeatures()
        self.hashData()
    def encodeQueryData(self,query_data):
        ndata = []

        qpre_data = [shingleText(row) for row in preProcessData(query_data)]
        queries = []
        for sdoc in qpre_data:
            tli = dict()
            for swrd in sdoc:
                if self.features.get(swrd,0):
                    tli[self.features[swrd]-1] = tli.get(self.features[swrd]-1,0) + 1
            queries.append(tli)
        for row in queries:
            trow = [0]*self.rfeature_size
            for i,id in enumerate(self.rfeatures):
                trow[i] += row.get(id,0)
            ndata.append(np.asarray(trow))
        return np.asarray(ndata)

    def randFeatures(self):
        self.rfeatures = np.random.randint(low = 0,high = len(self.features)-1,size = self.rfeature_size)
        self.rfeatures = self.rfeatures.tolist()
        self.rfeatures.extend(self.red_features)
        self.rfeatures = np.asarray(list(set(self.rfeatures)))
        self.rfeature_size = self.rfeatures.size

        for row in self.data:
            trow = [0]* self.rfeature_size
            for i,id in enumerate(self.rfeatures):
                trow[i] += row.get(id,0)
            self.rdata.append(np.asarray(trow))
        self.rdata = np.asarray(self.rdata)
        return None
    def getHash(self,x,table_id = 0, func_id = 0):
        hash_func = self.hsh_fn_tb[table_id]
        num_feature = len(x)
        if func_id not in hash_func:
            r = np.random.randn(num_feature)
            r = r / norm(r)
            hash_func[func_id] = r
        r = hash_func[func_id]
        hrdot = x.dot(r.T)
        return 1 if hrdot > 0 else 0

    def getSignature(self,x,table_id = 0):
        hash_key = ''
        for func_id in range(self.nfunc):
            hval = self.getHash(x,table_id,func_id)
            hash_key += '%d' % hval
        return hash_key
    def hashData(self):
        for i in range(self.rdata.shape[0]):
            crow = self.rdata[i,:]
            for table_id in range(self.ntabs):
                table = self.tables[table_id]
                hash_key = self.getSignature(crow,table_id)
                table.setdefault(hash_key,set()).add(i)
        return None
    @staticmethod
    def proximity(x,y):
        return x.dot(y.T)/(norm(x)*norm(y))

    def search(self, qdata, k = 5):
        candidates = set()
        for table_id in range(self.ntabs):
            table = self.tables[table_id]
            hash_key = self.getSignature(qdata,table_id)
            candidates = candidates.union(table[hash_key])
        similarity = [(i,self.proximity(self.rdata[i],qdata)) for i in candidates]
        self.nsims += len(similarity)
        similarity.sort(key = lambda x:x[1],reverse = True)
        k = min(k,len(similarity))
        return similarity[:k]
    

    def findSimDocs(self, qdata, k = 5):
        num_q = qdata.shape[0]
        #tmp_qdt = []
        #for row in qdata:
        #    tr = [0]*self.nfeatures
        #    for i,id in enumerate(self.rfeatures):
        #        tr[i] += row.get(id,0)
        #    tmp_qdt.append(np.asarray(tr))
        #qdata = np.asarray(tmp_qdt)
        
        nbrs = np.full((num_q,k),-1,dtype=np.double)
        nvals = np.zeros((num_q,k),dtype=np.double)
        self.nsims = 0
        for i in range(num_q):
            sims = self.search(qdata[i,:],k = k)
            nk = len(sims)
            if not nk:
                continue
            nbr,sim = zip(*sims)
            nbrs[i,:nk] = nbr
            nvals[i,:nk] = sim
        return nbrs,nvals