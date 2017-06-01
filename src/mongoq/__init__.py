from pymongo import MongoClient

# create connection to mongodb
CLIENT = MongoClient('mongodb://localhost:27017/')
DBNAME = 'test'
# get db
DB = CLIENT[DBNAME]
# get collection
DATA_CACHE_COLLECTION = DB.cache_queue