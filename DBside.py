import pymongo


class MyDatabase:

    def __init__(self, client_name, collection_name):
        self.client     = pymongo.MongoClient()
        self.database   = self.client[client_name]
        self.collection = self.database[collection_name]

    def save(self, data):
        self.collection.insert(data)

    def remove(self, data):
        self.collection.remove(data)
    
    def update(self, key, data):
        self.collection.update(key, data)

    def load(self, find = False):
        count           = 0
        documents       = []
        if find:
            datum       = self.collection.find(find)
        else:
            datum       = self.collection.find({})
        for document in datum:
            documents.append(document)
        return documents

    def log_out(self):
        self.client.close()
