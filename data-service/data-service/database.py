import pymongo


class Database(object):
    def save_item(self, dic):
        pass


class MongoDatabase(Database):
    def __init__(self, url, db_name, collection_name):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def drop(self):
        return self.collection.drop()

    def count(self):
        return self.collection.count()

    def find_one(self, dic):
        return self.collection.find_one(dic)

    def find_limit(self, dic, n):
        return self.collection.find(dic).limit(n)

    def update(self, dic):
        self.collection.save(dic)

    def delete(self, id):
        self.collection.remove(id)

    def save_item(self, dic):
        self.collection.insert_one(dic)

    def close(self):
        self.client.close()
