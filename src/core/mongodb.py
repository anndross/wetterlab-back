from pymongo import MongoClient 
from core.settings import MONGO_URI, MONGO_DATABASES
from pymongoarrow.api import Schema
import pymongoarrow.monkey
import bson

class MongoConnection: 
    def __init__(self, db_name):
        # Add extra find_* methods to pymongo collection objects:
        pymongoarrow.monkey.patch_all()
    
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.get_database(db_name)

    def get_collection(self, collection_name):
        return self.db.get_collection(collection_name)
        

meteor_connection = MongoConnection(MONGO_DATABASES.METEOR.value)
erp_connection = MongoConnection(MONGO_DATABASES.ERP.value)
