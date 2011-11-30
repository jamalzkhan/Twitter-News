import threading
import mongo_connector
import shared
import time
import datetime
import word_statistics
import sentiment_analysis

class Analysis(threading.Thread):
  def __init__(self,log,sleeptime=120,stories_col="stories",tweet_col="tweets"):
    threading.Thread.__init__(self)
    connector = mongo_connector.MongoConnector()
    self.stories_collection = connector.getCol(stories_col)
    self.tweet_collection = connector.getCol(tweet_col)
    self.word_stats = word_statistics.WordStatistics(self.tweet_collection)
    self.sentiment = sentiment_analysis.SentimentAnalysis(self.tweet_collection)
    self.last_update = datetime.datetime.utcnow()
    self.sleeptime = sleeptime
    self.log = log
  
  def run(self):
    while 1:
      #Sleep for sleeptime
      
      self.log.info("Sleeping for {0}.".format(self.sleeptime))
      time.sleep(self.sleeptime)
      
      self.add_stories_to_mongo(shared.stories)
      
      curr_time = datetime.datetime.utcnow()  
      self.add_new_time_period_to_stories(shared.stories, self.last_update, curr_time)
      self.last_update = curr_time


  def add_stories_to_mongo(self, stories):
    """Goes through a list of stories and adds them to the stories in mongo. 
    If story with this title is already there it just updates the date."""
    
    self.log.info("Adding extra stories to db.")
      
    for story in stories:
      in_db = self.stories_collection.find_one({"title": story["title"]})
      if not in_db:
        self.log.info("Story {0} is not in db. Adding...".format(story["title"]))
        story["update_time"] = time.time()
        story["created_at"] = time.time()
        self.stories_collection.insert(story)
      else:
        self.log.info("Story {0} is in db. Updating date.".format(story["title"]))
        in_db.update({"$set": {"date": story["date"]}})
        self.log.info("Story {0} is in db. Updating update_time.".format(story["title"]))
        in_db.update({"$set": {"update_time": time.time()}})
        self.log.info("Story {0} is in db. Updating keywords.".format(story["title"]))
        in_db.update({"$set": {"keywords": story["keywords"]}})
        self.log.info("Story {0} is in db. Updating link.".format(story["title"]))
        in_db.update({"$set": {"link": story["link"]}})
        self.log.info("Story {0} is in db. Updating main story link.".format(story["title"]))
        in_db.update({"$set": {"link_main_story": story["link_main_story"]}})
  
  def add_new_time_period_to_stories(self, stories, start, end):
    """Goes through tweets posted between start and end and assigns them to appropriate stories"""
    self.log.info("Adding time period from {0} to {1} to stories.".format(start,end))
      
    #Add time period stub to stories
    self.log.info("Adding curr_period to story objects")
    for story in stories:
      story["curr_period"] = {'period': end, 'tweets': []}
      
    #Loop through tweets
    self.log.info("Loading tweets from {0} to {1}.".format(start,end))
    tweets_in_time_period = self.tweet_collection.find({"created_at": {"$gte": start, "$lt": end}})
    for tweet in tweets_in_time_period:
      for story in stories:
        for keyword in story["keywords"]:
          keyword_words = keyword.split()
          if len(keyword_words) <= 0:
            continue;
          exists = True
          for keyword_word in keyword_words:
            exists = exists and (tweet["text"].find(keyword_word) != -1)
          if exists:
            story["curr_period"]["tweets"].append(tweet["_id"])
            break;
    
    self.log.info("Pushing new periods to db.")
      
    for story in stories:
      story["curr_period"]["wordstats"] = self.word_stats.get_word_statistics_for_tweets(story["curr_period"]["tweets"])
      story["curr_period"]["sentiment"] = self.sentiment.get_sentiment_for_tweets(story["curr_period"]["tweets"])
      
      self.log.info("Pushing period with {0} tweets to {1}".format(len(story["curr_period"]["tweets"]), story["title"]))
      self.stories_collection.update({"title":story["title"]},{"$push": {"periods": story["curr_period"]}})
