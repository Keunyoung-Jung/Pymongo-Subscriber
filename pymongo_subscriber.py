import os
import threading
import pandas as pd
import pymongo
from bson.objectid import ObjectId


class PymongoSubscriber:

    def __init__(self, _id, _password,cluster_name,db_name,collection_name):
        self.mongo_id = _id
        self.mongo_password = _password
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.collection_name = collection_name
        self.timeout = 15.0

        self._stop = False
        self._data_ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.daemon = True
        self._thread.start()

    def make_csv(self) :
        db_find = self.db[self.collection_name].find()
        data_frame = pd.DataFrame([],index=None,columns=[])
        for i in db_find:
            data_frame = pd.concat([data_frame,pd.DataFrame([dict(i)])])
            
        self._data = data_frame
        if len(data_frame) == 0 :
            print('Empty DB')
        else :
            data_frame.set_index('_id')
            data_frame.to_csv('./pymongo_db/{}_{}_{}.csv'.format(self.cluster_name,self.db_name,self.collection_name))
    
    def check_dir(self) :
        try:
            if not os.path.exists('./pymongo_db'):
                os.makedirs('./pymongo_db')
        except OSError:
            print ('Error: Creating directory. ' +  './pymongo_db')

    def _run(self):
        self.check_dir()

        mongo_client = pymongo.MongoClient(
            "mongodb+srv://{}:{}@{}.wboft.mongodb.net/{}?retryWrites=true&w=majority"\
                .format(self.mongo_id,self.mongo_password,self.cluster_name,self.db_name))

        self.db = mongo_client[self.db_name]
        pre_count = self.db[self.collection_name].count()
        self.make_csv()

        while not self._stop:
            count = self.db[self.collection_name].count()
            if not count == pre_count :
                self._data_ready.clear()
                self.make_csv()
            self._data_ready.set()

    def close(self):
        self._stop = True

    def timeoutError(self,flag) :
        if not flag:
            raise TimeoutError(
                "Timeout while reading from subscriber pymongo {}:{}".format(self.cluster_name, self.db_name))

    def receive_all(self):
        flag = self._data_ready.wait(timeout=self.timeout)
        self.timeoutError(flag)
        # self._data_ready.clear()
        return self._data

    def receive_first_one(self) :
        flag = self._data_ready.wait(timeout=self.timeout)
        self.timeoutError(flag)
        return self._data.iloc[0]

    def receive_last_one(self) :
        flag = self._data_ready.wait(timeout=self.timeout)
        self.timeoutError(flag)
        return self._data.iloc[len(self._data)-1]
    
    def receive_search(self,key,value) :
        flag = self._data_ready.wait(timeout=self.timeout)
        self.timeoutError(flag)
        return self._data.loc[self._data[key]==value]