
from snscrape.modules.twitter import TwitterSearchScraper
from datetime import datetime


def make_query(start_date: str, end_date: str, username: str=None, keyword: str=None):
    """Constructs a query string depending on the parameters supplied

    Args:
        start_date (str): the start date to begin scraping tweets from
        end_date (str): the end date for scraping tweets
        username (str, optional): a username, or user handle to scrape. Defaults to None.
        keyword (str, optional): a keyword or phrase to target during scrape. Defaults to None.
    """

    # form query string
    # based on whether the username and/or keyword is specified
    if username is None and keyword is not None:
        return f'{keyword} until:{end_date} since:{start_date}'

    elif username is not None and keyword is None:
        return f'(from:{username}) until:{end_date} since:{start_date}'

    elif username is not None and keyword is not None:
        return f"'{keyword}' (from:{username}) until:{end_date} since:{start_date}"

    else:
        raise KeyError('please specify a keyword or twitter@')
        



def historic_scrape(query, limit=200):
    """Gets the last 200 tweets from the specified query and returns them as a list.

    Args:
        query(str): a query string to find tweets
        limit(int): limit of the tweets, default to 200
    Returns:
        list: a list of the 200 tweets during period specified
    """
   
    tweets = []

    for tweet in TwitterSearchScraper(query).get_items():

        # if returned tweet hits the specified limit, then break the loop
        if len(tweets) == limit:
            break
        else:
            # else append the tweet to the list of tweets
            tweets.append({"date": tweet.date,
                           "source": tweet.user.username,
                           "text": tweet.content,
                           "date_scraped": datetime.now(),
                           "link": tweet.url})
    
    return tweets


def get_user_tl(twitter_api, username, tweet_count) -> list:
    """Gets the last n tweets from the specified user and returns them as a list.

    Args:
        twitter_api (api): tweepy api object
        username (str): tweeter username
        tweet_count (int): number of tweets to retrieve. maximum value is 300.

    Returns:
        list: a list of up to* the last 200 tweets
    """

    user_info = twitter_api.get_user(screen_name=username)

    # get the user's timeline
    user_tl = twitter_api.user_timeline(user_id=user_info.id, count=tweet_count, tweet_mode="extended", include_rts="false")

    # filter the timeline for tweets=oo
    results = [{"date": tweet.created_at.strftime("%m-%d-%Y"),
                "source": tweet.user.name,
                "text": tweet.full_text,
                "date_scraped": datetime.now().strftime("%m-%d-%Y")} 
                for tweet in user_tl]

    return results