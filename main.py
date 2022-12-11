

# consider implementing a dataclass for the data being scraped to ensure some level of consistency
# make query tests more
# # clean data of emoji and other impurities robust

# geolocate tweets?
# data schema for data going to the database to show relationships between fields
# deal with duplicate data
# different document in the collection for sources, and persons of interest
# update readme
# different database solution like HarperDB or Postgres
# automated and deployed





# class MyListener(tweepy.StreamingClient):
#     def on_data(self, data):
#       data_obj = json.loads(data.decode('utf8'))
#       print(json.dumps(data_obj,indent=2))
#       return True

#     def on_connect(self):
#       print('Connected..!')
        
#     def on_error(self, status):
#       print(status)
#       return True


# stream = MyListener(BEARER)
# stream.add_rules(tweepy.StreamRule('place:London OR place:Paris has:geo', tag="london-paris"))
# stream.filter(tweet_fields=["geo","created_at","author_id"],place_fields=["id","geo","name","country_code","place_type","full_name","country"],expansions=["geo.place_id"])




import os
from src.sources import twitter_scraper as twt
import tweepy
from pprint import pprint
from dotenv import load_dotenv
from src.database import send_to_db
load_dotenv()

API_Key = os.getenv("API_KEY")
API_Key_Secret = os.getenv("API_KEY_SECRET")
Access_Token = os.getenv("ACCESS_TOKEN")
Access_Token_Secret = os.getenv("ACCESS_TOKEN_SECRET")



auth = tweepy.OAuth1UserHandler(API_Key, API_Key_Secret, Access_Token, Access_Token_Secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

starts = "2022-06-01"
ends = "2022-12-09"





if __name__ == '__main__':
    # query = twt.make_query(starts, ends, 'namedToobi', 'Elon')
    # results = twt.historic_scrape(query=query, limit=10)

    resultants = twt.get_user_tl(api, 'namedToobi', 2)
    pprint(resultants)
    # send_to_db(resultants, 'election_data', 'twitter_scrape')
    
    