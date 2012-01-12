import datetime, json, time, pymongo
from pymongo import objectid

class Database:
  def __init__(self,host='localhost',port=27017):
    # Configuration
    self.MONGODB_HOST = host
    self.MONGODB_PORT = port
    
    # Defining database and collections
    self.database_name = "twitter_news"
    self.story_collection_name = "stories"
    
    # Connection to the database and collections
    self.connection = pymongo.Connection(self.MONGODB_HOST, self.MONGODB_PORT)
    self.database = self.connection[self.database_name]
    self.stories = self.database[self.story_collection_name]
  

  def getStoriesAddedAfterTimestamp(self, time_stamp):
    """Used to get the most recent stories since the given timestamp"""
    stories_array = []
    for story in self.stories.find({'date_added' : { '$gt': time_stamp }}).sort('date_added', -1):
      stories_array.append(str(story["_id"]))
    stories = {'news': stories_array, 'requesttime' : time.time(), }
    return stories
  
  def getStoriesAddedBeforeTimestamp(self, time_stamp, no_of_stories=10):
    stories_array = []
    before_timestamp = 0
    timestamp_set = False
    for story in self.stories.find({'date_added' : { '$lt': time_stamp }}).sort('date_added', direction=pymongo.DESCENDING).limit(no_of_stories):
      if (not timestamp_set):
        before_timestamp = story["date_added"]
        timestamp_set = True
      elif (before_timestamp > story["date_added"]):
        before_timestamp = story["date_added"]
      stories_array.append(str(story["_id"]))
    stories_array.reverse()
    stories = {'news': stories_array, 'requesttime': time.time(), 'bottomtimestamp': before_timestamp}
    return stories
  
  def getRecentStories(self, no_of_stories=10):
    """Used to get the most recent stories in json format {news: [story_1, story_2,..,story_number_of_stories]}"""
    stories_array = []
    bottom_timestamp = 0
    top_timestamp = 0
    timestamps_set = False
    for story in self.stories.find().sort('date_added', direction=pymongo.DESCENDING).limit(no_of_stories):
      if (not timestamps_set):
        bottom_timestamp = story["date_added"]
        top_timestamp = story["date_added"]
        timestamps_set = True
      elif (bottom_timestamp > story["date_added"]):
        bottom_timestamp = story["date_added"]
      elif (top_timestamp < story["date_added"]):
        top_timestamp = story["date_added"]
      stories_array.append(str(story["_id"]))
    stories_array.reverse()
    stories = {'news': stories_array, 'requesttime' : time.time(), 'bottomtimestamp': bottom_timestamp, 'toptimestamp': top_timestamp}
    return stories
    
  def getStory(self, story_id):
    """Given the story id gives a story summary, along with tweet data for the most recent time period"""
    try:
      id = objectid.ObjectId(str(story_id))
    except objectid.InvalidId:
      return {'error' : 'Invalid Id'}
    story = self.stories.find_one({'_id':id})  
    if story != None:
      return {
        'title': story["title"], 
        'summary': story["summary"], 
        'link': story["link_main_story"], 
        'keywords': story["keywords"], 
        'wordcloud': Database.combineWordclouds(story["periods"]),
        'sentiment' : Database.combineSentiment(story["periods"]),
        'tweets': map(lambda x: {"user": x["user"], "text" : x["text"], "score" : x["score"]}, story["periods"][-1]["tweets"] ) }
    else:
      return {'error' : 'Story does not exist'}
        
  def getStories(self):
    """Used to get all the stories"""
    stories = []
    for story in self.stories.find():
      stories.append(story["title"])
    return stories
    
  
  @staticmethod
  def combineWordclouds(periods):
    res = {}
    for period in periods:
      for word,val in period["wordstats"].iteritems():
        if word in res:
          res[word] = res[word] + val
        else:
          res[word] = val
    return res
        
  
  @staticmethod
  def combineSentiment(periods):
    res = {}
    for period in periods:
      for word,val in period["sentiment"].iteritems():
        if word in res:
          res[word] = res[word] + val
        else:
          res[word] = val
    return res
  

if __name__ == "__main__":
  d = Database()
  print d.getRecentStories(10)
  # print d.getStory("4eb428e91786f0117a000003")
  # print d.getStoriesByTimeStamp(time)
  
