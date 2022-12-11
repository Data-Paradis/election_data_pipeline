import pytest
from src.sources.twitter_scraper import make_query, historic_scrape, get_user_tl
from snscrape.modules.twitter import TwitterSearchScraper
from types import SimpleNamespace
from tweepy import API, OAuth1UserHandler 
from datetime import datetime as dt

class NestedNamespace(SimpleNamespace):
    """Expands the name space functionality to support nested dictionaries

    Args:
        SimpleNamespace (_type_): A simple name space object
    """
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        # change the namedspace init function to get the nested dictionaries
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


# Arrange
@pytest.fixture
def approx_content():
    """Fixture that returns an approximation of the response of the scraper

    Returns:
        list: list of content blocks
    """
    # similar content structure
    content = {"date": "some date",
               "content": "some content",
               "url": "some url", 
               "user": {"username": "Random User",}}

    # change type from dict to NamedSpace
    result = NestedNamespace(content)

    return [result, result, result, result, result, result, result, result, result, result, result, result, result]


def test_make_query_no_keyword_with_username():
    """Tests the make_query function when no keyword is specified
        but a username is given
    """
    starts = "2022-06-01"
    ends = "2022-12-09"
    query = make_query(starts, ends, 'random_user')
    assert 'random_user' and starts and ends in query
    


def test_make_query_no_username_with_keyword():
    """Tests the make_query function with a keyword and no username specified
    """
    starts = "2022-06-01"
    ends = "2022-12-09"
    query = make_query(starts, ends, keyword='python')
    assert 'random_user' and starts and ends in query
    


def test_make_query_no_username_and_keyword():
    """Tests the make_query function with no username and keyword
    """
    starts = "2022-06-01"
    ends = "2022-12-09"
    with pytest.raises(KeyError):
        query = make_query(starts, ends)
    


def test_make_query_with_keyword_and_username():
    """Tests the make_query function with keyword and username
    """
    starts = "2022-06-01"
    ends = "2022-12-09"
    query = make_query(starts, ends, 'random_user', 'python')
    assert 'random_user' and starts and ends and 'python' in query


def test_historic_scrape(monkeypatch, approx_content) -> None:
    """
    Tests the default behavior of the historic_scrape() method."""
    
    # test parameters
    test_date_start = "2022-05-17"
    test_date_end = "2022-06-15"
    keyword = "weird"
    username = "Random User"

    my_query = make_query(test_date_start, test_date_end, username, keyword)

    # add content as return value of Twitter Search Scraper get items
    monkeypatch.setattr(TwitterSearchScraper, "get_items", lambda query: approx_content)

    # call functionality
    test_return = historic_scrape(my_query)

    # assertions
    assert type(test_return) == list
    assert "date" in list(test_return[0].keys())
    assert "source" in list(test_return[0].keys())
    assert "text" in list(test_return[0].keys())
    assert "link" in list(test_return[0].keys())
    assert str == type(test_return[0]["source"])
    assert username == test_return[0]["source"]


def test_historic_scrape_limit(monkeypatch, approx_content) -> None:
    """Tests the historic_scrape() method with a limit.
    """

     # test parameters
    test_date_start = "2022-05-17"
    test_date_end = "2022-06-15"
    keyword = "weird"
    username = "Random User"

    my_query = make_query(test_date_start, test_date_end, username, keyword)

    # add content as return value of Twitter Search Scraper get items
    monkeypatch.setattr(TwitterSearchScraper, "get_items", lambda query: approx_content)

     # call functionality
    test_return = historic_scrape(my_query, limit=5)

    # assertions
    assert type(test_return) == list
    assert len(test_return) == 5
    assert "date" in list(test_return[0].keys())
    assert "source" in list(test_return[0].keys())
    assert "text" in list(test_return[0].keys())
    assert "link" in list(test_return[0].keys())
    assert str == type(test_return[0]["source"])


def test_get_user_tl(monkeypatch):
    """Tests the tweet streaming functionality"""

    # similar content structure
    content = {"created_at": dt.now(),
               "full_text": "some content",
               "url": "some url", 
               "user": {"name": "Random User",}}

    # change type from dict to NamedSpace
    result = NestedNamespace(content)

    # make a user object
    user_details = {"id": [12345678]}

    # convert the user object to a namedspace
    user_named_space = SimpleNamespace(**user_details)

    # make expected content
    content_payload = [result, result, result, result, result, result, result, result, result, result, result, result, result]

    # mock the get user and user time line function calls
    monkeypatch.setattr(API, "get_user", lambda *args, **kwargs: user_named_space)
    monkeypatch.setattr(API, "user_timeline", lambda *args, **kwargs: content_payload)

    # make a dummy auth and api object
    faux_auth = OAuth1UserHandler("api_key", "api_key_secret", "access_token", "access_token_secret")
    test_api = API(faux_auth, wait_on_rate_limit=True)

    # call the function to be tested
    test_results = get_user_tl(twitter_api=test_api, tweet_count=2, username="Random User")

    assert list == type(test_results)
    assert "date" in list(test_results[0].keys())
    assert "source" in list(test_results[0].keys())
    assert "text" in list(test_results[0].keys())
    assert str == type(test_results[0]["text"])
    assert "Random User" == test_results[0]["source"]