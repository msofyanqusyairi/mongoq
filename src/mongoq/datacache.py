#!/usr/bin/env python

# #############################################################################
# (c) 2017
# dev: Muhammad Sofyan Qusyairi , sofyanqusyairi@gmail.com
#
# Description:
# make thread-receive and thread-send, to manage traffic data to entry inside the mongo_queue
#
# LISENSI CODE: see file 'LICENSE.txt'
# #############################################################################

import threading
import json
from mongoq import MongoQueue
import time

LEN_DATA_CACHE = 0

class CacheController:
    def __init__(self, processId, delayReceive, delaySend):
        self.__dataCacheQueue = MongoQueue(
            processId = processId
            )
        self.__threadReceive = ThreadReceive(self.__dataCacheQueue, delayReceive)
        self.__threadSend = ThreadSend(self.__dataCacheQueue, delaySend)

    def getThreadReceive(self):
        return self.__threadReceive

    def getThreadSend(self):
        return self.__threadSend

    def startThreadSend(self):
        # start thread ThreadSend
        self.__threadSend.start()

    def startThreadReceive(self):
        # start thread ThreadReceive
        self.__threadReceive.start()

# thread for receive
# insert data to mongo queue
class ThreadReceive(threading.Thread):
    def __init__(self, dataCache, delay=1):
        threading.Thread.__init__(self)
        self.__delay = delay
        self.__dataCache = dataCache
        # init queuing data
        self.__dataContent = []

    def appendData(self, dataContent):
        # queuing data
        print '-- append data content --'
        self.__dataContent.append({'data_cache':dataContent})

    # save data cache to memory
    def __saveData(self):
        # inside try-except block
        print 'len queue %s' % (len(self.__dataContent))
        # get first element
        if (len(self.__dataContent) > 0):
            print 'save data cache'
            # fetch first element list
            dataContent = self.__dataContent[0]
            # put __dataContent to mongoqueue
            self.__dataCache.put(dataContent)
            # update LEN DATA CACHE
            LEN_DATA_CACHE = self.__dataCache.getSize()
            # pop first element (ignore if __dataCache.put is getting exception)
            self.__dataContent.pop(0)
    
    # override threading
    def run(self):
        # while True
        while True:
            try:
                # __saveData (blocking)
                print '-- trying check queue --'
                self.__saveData()
            except Exception as e:
                print 'Exception info: %s' % e
            # delay
            time.sleep(self.__delay)

# thread for send
# fetch data from mongo queue and send to internet
class ThreadSend(threading.Thread):
    def __init__(self, dataCache, system, delay=1):
        threading.Thread.__init__(self)
        self.__delay = delay
        self.__dataCache = dataCache
        self.__system = system
        self.__fetchStatus = False
    
    # open data cache from memory
    def __fetchData(self):
        # next queue cursor
        job = self.__dataCache.getJobReady()
        print 'fetched data from locked_at: %s' % job.getLockedAt()
        # return payload
        return job.getPayload()

    def __nextCursor(self):
        # set fetch status to False,
        # it means another process has get the data
        self.__dataCache.next()
        self.__fetchStatus = False

    # send data cache to another process
    def throw(self, func, param):
        # flag is output (True or False)
        # if True, it means another process has get the data.
        # and below to inform ThreadSend (Ack to ThreadSend)
        flag = func(*param)
        if flag:
            self.__fetchStatus = True

    # override threading
    def run(self):
        # while true
        while True:            
            #try
            try:
                # fetch data
                dataReady = self.__fetchData()['data_cache']
                content = dataReady['content']
                if dataReady and self.__fetchStatus:
                    # next cursor in queue 
                    # if data ready is not none, and another process accept to get data
                    self.__nextCursor()
                        

            # except
            except (NameError, TypeError):
                print "Mongo queue is empty"
            except Exception as e:
                print 'Exception info: %s' % e
            # delay
            time.sleep(self.__delay)