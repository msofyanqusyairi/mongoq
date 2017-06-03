#!/usr/bin/env python

# #############################################################################
# (c) 2017
# dev: Muhammad Sofyan Qusyairi , sofyanqusyairi@gmail.com
#
# Description: make a queue inside mongodb
#
# LISENSI CODE: see file 'LICENSE.txt'
# #############################################################################


from datetime import datetime
import pymongo
from cachequeue import DATA_CACHE_COLLECTION



class MongoQueue:
    def __init__(self, processId):
        self.__collection = DATA_CACHE_COLLECTION
        self.__processId = processId

    def put(self, payload):
        # Put data to mongo queue, represented insert to queue
        jobData = dict({})
        jobData['locked_by'] = self.__processId
        jobData['locked_at'] = datetime.now()
        jobData['payload'] = payload
        self.__collection.insert_one(jobData)

    def getJobReady(self):
        # find one and delete (sort ascending by time), represented pull from queue
        jobData = self.__collection.find_one(
                filter = {},
                sort = [('locked_at', pymongo.ASCENDING)]
            )
        job = Job(jobData)
        return job

    def getSize(self):
        # get size of queue
        return self.__collection.count()

    def next(self):
        # Next cursor in queue list
        self.__collection.find_one_and_delete(
                filter = {},
                sort = [('locked_at', pymongo.ASCENDING)]
            )
        print '-- next cursor --'

    def clear(self):
        # clear collection, represented clear the queue
        self.__collection.delete({})

class Job:
    def __init__(self, data):
        # locked_by is something that performs queue input (auto create)
        # locked_at is to explain when the locked_by performs queue input (auto create)
        # payload is originally data (create by input program)
        self.__lockedBy = data['locked_by']
        self.__lockedAt = data['locked_at']
        self.__payload = data['payload']

    def getLockedBy(self):
        return self.__lockedBy

    def getLockedAt(self):
        return self.__lockedAt

    def getPayload(self):
        return self.__payload