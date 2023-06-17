from dataFetchers import *
from dbManager import MongodbCollectionManager

def fillData(real_time_db, mongo_client, tokens, configurations):
    # Iterate through configurations
    for collection_name, (fetcher, args) in configurations.items():          
        data = fetcher(*args)
        # print(type(data))
        collection_manager = MongodbCollectionManager(mongo_client, real_time_db, collection_name)
        if data is None:
            if collection_name == "openUV":
                if not tokens:
                    print("No more tokens available for openUV API")
                    continue
                openuvtoken = tokens.pop()
                args[0] = openuvtoken
                data = fetcher(*args)
                collection_manager = MongodbCollectionManager(mongo_client, real_time_db, collection_name)
            else:
                print(f"Error: {collection_name} data is None")
                continue
        collection_manager.store_data(data)
        