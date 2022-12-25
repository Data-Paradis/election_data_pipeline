
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
load_dotenv()

my_db = os.getenv("MONGODB_ATLAS")
client = MongoClient(my_db)



def send_to_db(data, collection_name, doc_name):

    my_collection = client[collection_name]
    zone_collection = my_collection[doc_name]
    try:
        zone_collection.insert_many(data)
        print('done with data push')
    except Exception as e:
        print(f'database push failed with exception {e}')


if __name__ == '__main__':
    my_collection = client['election_data']
    my_collection['twitter_scrape'].create_index([("source", pymongo.DESCENDING),
                            ("link", pymongo.ASCENDING)])