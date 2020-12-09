import os
import threading
import pandas as pd
import pymongo
from bson.objectid import ObjectId


class PymongoSubscriber:
    '''
    Pymongo subscriber :  pymongo is very slow when used in python, 
    this code is similar to pub/sub, trying to subscribe to pymongo data in real time without affecting your code.
    
    Author : Keyog Jung
    Date : 2020.11.30

    Example
    mongo_reader = PymongoSubscriber(
        mid='admin',
        password='admin',
        cluster_name='cluster',
        db_name='database',
        collection_name='collection')
    '''
    def __init__(self, mid, password,cluster_name,db_name,collection_name,make_csv=True):
        '''
        Connect mongoDB with pymongo
        '''
        self._mongo_id = mid
        self._mongo_password = password
        self._cluster_name = cluster_name
        self._db_name = db_name
        self._collection_name = collection_name
        self._timeout = 15.0
        self._data = pd.DataFrame()
        self._make_csv = make_csv

        self._stop = False
        self._data_ready = threading.Event()
        self._thread = threading.Thread(target=self._run, args=())
        self._thread.daemon = True
        self._thread.start()

    def __str__(self) :
        '''
        Return Current Connected DB information
        '''
        return f'Connected MongoDB Info \nID:{self._mongo_id}\nDB_Info:{self._cluster_name}>{self._db_name}>{self._collection_name}'

    def get_data(self,mongo_client) :
        '''
        Get data from MongoDB and Convert Cursor Object to DataFrame
        '''
        return pd.concat([pd.DataFrame([dict(x)]) 
                            for x in mongo_client[self._db_name][self._collection_name].find()])

    def make_csv(self) :
        '''
        Make csv file from mongoDB DataFrame
        '''
        if len(self._data) == 0 :
            print('Empty DB')
        else :
            self._data.to_csv(f'./pymongo_db/{self._cluster_name}_{self._db_name}_{self._collection_name}.csv')
    
    def check_dir(self) :
        '''
        Create a directory to store the DataFrame csv
        '''
        try:
            if not os.path.exists('./pymongo_db'):
                os.makedirs('./pymongo_db')
        except OSError:
            print ('Error: Creating directory. ' +  './pymongo_db')

    def _run(self):
        '''
        Reading MongoDB on Thread
        '''
        mongo_client = pymongo.MongoClient(
            "mongodb+srv://{}:{}@{}.wboft.mongodb.net/{}?retryWrites=true&w=majority"\
                .format(self._mongo_id,self._mongo_password,self._cluster_name,self._db_name))

        pre_count = mongo_client[self._db_name][self._collection_name].count()
        self._data = self.get_data(mongo_client)
        if self._make_csv :
            self.check_dir()
            self.make_csv()

        while not self._stop:
            if not mongo_client[self._db_name][self._collection_name].count() == pre_count :
                self._data_ready.clear()
                self.get_data(mongo_client)
                if self._make_csv :
                    self.make_csv()
            self._data_ready.set()

    def close(self):
        '''
        Disconnect mongoDB with pymongo
        '''
        self._stop = True

    def timeoutError(self,flag) :
        if not flag:
            raise TimeoutError(
                "Timeout while reading from subscriber pymongo {}:{}".format(self._cluster_name, self._db_name))

    def receive_all(self):
        '''
        receives All mongoDB data in the form of a data DataFrame 
        '''
        flag = self._data_ready.wait(timeout=self._timeout)
        self.timeoutError(flag)
        # self._data_ready.clear()
        return self._data

    def receive_first_one(self) :
        '''
        receives first one data in the form of a data DataFrame 
        '''
        flag = self._data_ready.wait(timeout=self._timeout)
        self.timeoutError(flag)
        return self._data.iloc[0]

    def receive_last_one(self) :
        '''
        receives last one data in the form of a data DataFrame 
        '''
        flag = self._data_ready.wait(timeout=self._timeout)
        self.timeoutError(flag)
        return self._data.iloc[len(self._data)-1]
    
    def receive_search(self,key,value) :
        '''
        receives each data using search in the form of a data DataFrame 
        '''
        flag = self._data_ready.wait(timeout=self._timeout)
        self.timeoutError(flag)
        return self._data.loc[self._data[key]==value]