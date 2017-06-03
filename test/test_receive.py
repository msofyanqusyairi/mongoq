from bottle import post, request, run

# This is test module as receiver, to test receive data to mongoq

# Triggering by HTTP POST
@post('/emit')
def emittest():
    print "Receive: {0}".format(request.body.read())

# run app server
run(host='0.0.0.0', port='3001', debug=True)