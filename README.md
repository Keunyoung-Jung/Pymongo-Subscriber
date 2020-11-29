# Pymongo-Subscriber
 pymongo is very slow when used in python, this code is similar to pub/sub, trying to subscribe to pymongo data in real time without affecting your code.
 
# Dependencies
* bson
* pymongo
* dnspython
* pandas

# Why the code was written
This code helps to use MongoDB on the cloud server in Python.    
If pymongo is used as it is in python, it is too slow.   
If you are going to create a real-time service using pymongo, it may not be possible to implement it using the default pymongo.    
So, I got the idea from the sub/pub method and I want to be able to use pymongo on python in real time.    

# Prepare for use
 
# Speed compare
## Find data comparison
Test after loading mongo client in advance    
| | Default pymongo | Pymongo-Subscriber(This code) |
|:-----:|--------:|--------:|
| Find first data 100 times| 19.32sec | **0.02sec** |
| Find last data 100 times | 19.31sec | **0.015sec** |
| Find data using query 100K data | *Ready..* | *Ready..* |
| Insert one data | 1.57sec | **0.31sec** |
   
*However, since the insert method is dependent on pymongo, it takes the same time to be reflected in the cloud server.    
Nevertheless, because the data in the buffer db is updated without an id, it is possible to load and use the data.*      


# How to use this code
### Create Receiver variable
```python
mongo_receiver = PymongoSubscriber(
    _id='admin',
    _password='admin',
    cluster_name='order',
    db_name='testDB',
    collection_name='testCOL')
```
### Function information
Shutdown data receiver : `mongo_receiver.close()`    
Forced update Buffer DB
```python
mongo_receiver.update()
```
Return All of data (pandas Dataframe type)
```python
mongo_receiver.receive_all()
```
----
Return first data (pandas Dataframe type)
```python
mongo_receiver.receive_first_one()
```
Return last data (pandas Dataframe type)
```python
mongo_receiver.receive_last_one()
```
Return find data using query (pandas Dataframe type)
```python
mongo_receiver.receive_search(key,value)
```
Insert one data on MongoDB
```python
mongo_receiver.insert_one_mongo(data)
```
Insert many data on MongoDB
```python
mongo_receiver.insert_many_mongo(data)
```

# To do
- [x] Use Thread
- [x] Create Dataframe
- [x] Link MongoDB
- [x] Event handler
- [x] Create example code
- [x] Receive MongoDB data
- [x] Receive Real-time
- [x] Receive function (first,last,search)
- [ ] Queries with regular expressions
- [ ] Receive many data
- [ ] Send insert Event
- [ ] Send Update Event
- [ ] Send Delete Event
- [ ] Write comments
- [ ] Upgrading monitering MongoDB method
