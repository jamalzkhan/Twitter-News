import urllib2, urllib
import json
import unicodedata

class SentimentAnalysis:
  def __init__(self,tweet_collection):
    self.tweet_collection = tweet_collection
    self.API_LINK = "http://twittersentiment.appspot.com/api/bulkClassifyJson"
    self.HEADERS = { "Content-Type": "application/json" }
  
  def get_sentiment_for_tweets(self, tweets):
    """Return sentiment for the array of tweet ids supplied"""
    tweet_text_list = []
    for tweet_id in tweets:
      text_ascii =  unicodedata.normalize('NFKD', self.tweet_collection.find_one({"_id" : tweet_id }, {"text" : 1})['text']).encode('ascii','ignore')
      tweet_text_list.append( {'text': text_ascii, 'tid': tweet_id } )

    data = { 'data' : tweet_text_list }
    req = urllib2.Request(self.API_LINK, headers = self.HEADERS, data = str(data) )
    f = urllib2.urlopen(req)
    response = f.read()
    response_json = json.loads(response)

    result = {'positive' : 0, 'neutral' : 0, 'negative' : 0}

    for r in response_json["data"]:
      pol = r["polarity"]
      if pol == 4:
        result['positive'] += 1
      elif pol == 2:
        result['neutral'] += 1
      elif pol == 0:
        result['negative'] += 1

    return result