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
### Find first data 10 times
### Find last data 10 times
### Find data using query 100K data

## Insert data comparison
### Insert 100K data

# How to use this code

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
