import pymongo


class MongoDatabase:
    def __init__(self, url=None, db_name=None, collection_name=None):
        self.url = "172.104.110.189:27017"
        self.db_name = "fxstorage"
        self.collection_name = "strategy"

        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def drop(self):
        return self.collection.drop()

    def count(self):
        return self.collection.count()

    def find_one(self, dic):
        return self.collection.find_one(dic)

    def find_limit(self, dic, n):
        return self.collection.find(dic).limit(n)

    def find_all(self, dic):
        return self.collection.find(dic)

    def update(self, dic):
        self.collection.save(dic)

    def delete(self, id):
        self.collection.remove(id)

    def delete_all(self):
        self.collection.remove({})

    def save_item(self, dic):
        return self.collection.insert_one(dic)

    def close(self):
        self.client.close()
