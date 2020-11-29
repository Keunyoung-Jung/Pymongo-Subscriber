from pymongo_subscriber import PymongoSubscriber
import pandas as pd
import time
import datetime

mongo_receiver = PymongoSubscriber(
    _id='admin',
    _password='admin',
    cluster_name='order',
    db_name='toppingtable',
    collection_name='order_list')

# while True :
last = mongo_receiver.receive_last_one()
print(last['menu'])

data = {
    'menu':"Sweet_potato",
    'store':"100th store",
    'time':datetime.datetime.now(),
    'cpu_time':time.time()
}
st = time.time()
mongo_receiver.insert_one_mongo(data)
print(1/(time.time()-st))
# last = mongo_receiver.receive_last_one()
# mongo_receiver.insert_one_mongo(data)
# # mongo_receiver.insert_one_mongo(data)

# last = mongo_receiver.receive_last_one()
# print(last)
    # time.sleep(1)
    # st = time.time()
    # df = mongo_receiver.receive_all()
    # print('df')

    # first = mongo_receiver.receive_first_one()
    # last = mongo_receiver.receive_last_one()
    # print('first')

    # print('last')
    # search = mongo_receiver.receive_search(key='TOT_AMT',value='6900')
    # print(search)
    # print('fps :',1/(time.time()-st)