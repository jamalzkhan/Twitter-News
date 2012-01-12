import re
import collections

class WordStatistics:
  def __init__(self,tweet_collection,min_len=3,max_len=20,limit=30):
    self.min_len = min_len
    self.max_len = max_len
    self.word_limit = limit
    self.tweet_collection = tweet_collection
    self.blacklist = [line.strip() for line in open('word_statistics_blacklist.txt')]
  
  def get_word_statistics_for_tweets(self, tweets):
    """Returns word statistics for the array of tweet ids supplied"""
    tweet_text_list = []
    for tweet_id in tweets:
      tweet_text_list.append(self.tweet_collection.find_one({"_id" : tweet_id}, {"text" : 1})['text'])
    text = " ".join([k for k in tweet_text_list]).lower()
    words = [w for w in re.findall("\w{3,20}",text) if w not in self.blacklist]
    return dict(collections.Counter(words).most_common(self.word_limit))
    