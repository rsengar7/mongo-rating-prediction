from pymongo import MongoClient

class MongoDBConnection():
    """
    Class to establish a connection to MongoDB and fetch data.
    """
    def __init__(self, host='localhost', port=27017, db_name=None, collection_name=None):
        # Initialize MongoDB connection
        self.client = MongoClient(f'{host}:{port}')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_data(self, query={}):
        """
        Method to fetch data from MongoDB.
        """
        cursor = self.collection.find(query)
        data_list = list(cursor)
        return data_list

    def insert_one(self, document):
        """
        Insert a single document into the collection.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def insert_many(self, documents):
        """
        Insert multiple documents into the collection.
        """
        result = self.collection.insert_many(documents)
        return result.inserted_ids