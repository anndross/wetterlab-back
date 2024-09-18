from pymongo import MongoClient 
from core.settings import MONGO_URI, MONGO_DATABASES

class MongoConnection: 
    def __init__(self, db_name):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

meteor_connection = MongoConnection(MONGO_DATABASES.METEOR.value)
erp_connection = MongoConnection(MONGO_DATABASES.ERP.value)
