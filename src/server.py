#!/usr/bin/env python

# #############################################################################
# (c) 2017
# dev: Muhammad Sofyan Qusyairi , sofyanqusyairi@gmail.com
#
# Description: 
# Server for make data cache using mongodb, and make mongodb as queue
# 
#
# LISENSI CODE: see file 'LICENSE.txt'
# #############################################################################

import bottle
from bottle import post, request, run
import json

from cachequeue.datacache import CacheController

# init cache
processId = "process-1"
delayReceive = 5
delaySend = 5
cacheController = CacheController(processId, delayReceive, delaySend)

# start thread
cacheController.startThreadReceive()
cacheController.startThreadSend()

# HTTP REST API

# chacing data channel http post
@post('/caching')
def caching():
    print '-- POST Request --'
    # request body forms (payload)
    data = request.body.read()
    dataContent = json.loads(data)
    newData = dataContent['content']
    url = dataContent['url']
    timeout = dataContent['timeout']
    fixContent = {
        'content' :  newData,
        'url' : url,
        'timeout' : timeout
    }
    
    cacheController.getThreadReceive().appendData(fixContent)

# end

# end

# debug mode
# run server
run(host='0.0.0.0', port=3000, debug=True)