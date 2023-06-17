class MongodbCollectionManager:
    def __init__(self, mongo_client, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongo_client = mongo_client
        self.db = self.mongo_client[self.db_name]
        self.collection = self.db[self.collection_name]

    def store_data(self, data):
        try:
            if type(data) is dict:
                self.collection.insert_one(data)
            elif type(data) is list:
                self.collection.insert_many(data)
            else:
                raise TypeError("data must be a dict or a list")
        except Exception as e:
            print(e)             
        
    def get_last_added_item(self):
        return self.collection.find().sort("_id", -1).limit(1)[0]

    def get_items_by_query(self, query):
        return self.collection.find(query)
