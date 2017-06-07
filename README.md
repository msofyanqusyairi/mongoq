# MongoQ

## Description
* Simplicity to use mongodb with FIFO mechanism (Queue)
* With this module, can store FIFO cache data, to transfer data from one server/process to another server/process (While, this module support for HTTP communication)

## Requirement
* bottle (>=0.12.13)
* simple-json (>=1.1)
* simplejson (>=3.10.0)

## DATA SENDER
* Data is sent using HTTP protocol (can be adjusted)
* Header: {'Content-type': 'application/json', 'Accept': 'text/plain'} --> (can be adjusted)
* payload : {'content': '[data]', 'url':'http://[host-server]', 'timeout':[timeout]}

## DATA RECEIVER
* The receiver will receive data {'payload': {'content': [data]}}

## DATA CACHE in MongoQ
* This module provides 2 thread.
    * Thread Receive : Receive data from sender, then insert to mongodb
    *Thread Send : find and delete data from mongodb, check and send data to another server/process