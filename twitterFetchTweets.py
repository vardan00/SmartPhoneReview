"""
    twitterFetchTweets.py - Get twitter data using Api
"""

import twitter
import re
from keys import key

k = key()
api = twitter.Api(consumer_key=k.consumer_key,
                      consumer_secret=k.consumer_secret,
                      access_token_key=k.access_token_key,
                      access_token_secret=k.access_token_secret,
                      tweet_mode='extended')

def remove_emoji_links(string):
    """Remvoes the emoji links

    :param string: The tweets
    :returns: A string with no emojis
    :rtype: string
    """
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    
    string = emoji_pattern.sub(r'', string)
    return re.sub(r"http\S+", "", string)

def twitter_search( q, max_results=1000, **kw):
    """searches the tweets

    :param q: input search term(model name)
    :param max_results: Total number of results per request
    :returns: the list of tweets
    :rtype: list of strings

    """
    search_results = api.GetSearch(term=q +" -filter:retweets AND -filter:replies",count=100,lang='en')
    statuses = search_results
    for _ in range(10): # 10*100 = 1000
        try:
            val = search_results[-1].AsDict()
            since_id =   val['id']
        except: # No more results when next_results doesn't exist
            print("No more results")
            break
        search_results = api.GetSearch(term=q+" -filter:retweets AND -filter:replies",count=100,lang='en',since_id=since_id)
        statuses += search_results
        if len(statuses) > max_results:
            break
    
    return statuses

tweets=[]
def searchSmartPhone(mobile):
    """ Return Pre processed tweets

    :param mobile: the mobile model name
    :returns: list of cleaned tweets( no emojis and lins)
    :rtype: list of strings

    """
    global tweets
    print(mobile)
    results =  twitter_search(mobile)
    for result in results:
        result = result.AsDict()
        cleaned_tweet = remove_emoji_links(result['full_text']).lower()
        tweets.append(cleaned_tweet)
    return tweets
