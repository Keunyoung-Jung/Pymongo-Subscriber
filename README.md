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
### Find first data 100 times
*Default pymongo*
Input : 
```python
for i in range(100) :
    db[collection_name].find_one()
```
Output :
```
time : 19.329524755477905 second
```
*Use Pymongo-Subscriber*
Input : 
```python
for i in range(100) :
    mongo_receiver.receive_first_one()
```
Output :
```
time : 0.02027297019958496 second
```



### Find last data 100 times
*Default pymongo*
Input : 
```python
st = time.time()
for i in range(100) :
    db[collection_name].find_one()
print('time : {} second'.format(time.time()-st))
```
Output :
```
time : 19.313278675079346 second
```
*Use Pymongo-Subscriber*
Input : 
```python
st = time.time()
for i in range(100) :
    mongo_receiver.receive_last_one()
print('time : {} second'.format(time.time()-st))
```
Output :
```
time : 0.015398502349853516 second
```

### Find data using query 100K data

## Insert data comparison
### Insert 100K data

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
