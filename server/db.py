import datetime, json, time
from pymongo import Connection
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
    self.connection = Connection(self.MONGODB_HOST, self.MONGODB_PORT)
    self.database = self.connection[self.database_name]
    self.stories = self.database[self.story_collection_name]
  
  
  def getStoriesByTimeStamp(self, no_of_stories=10, time_stamp=time.time()):
    """Used to get the most recent stories since the given timestamp"""
    stories_array = []
    for story in self.stories.find({'api_time' : { '$lte': time_stamp }}).sort('api_time'):
      stories_array.append(str(story["_id"]))
      stories = {'news': stories_array}
      return stories
    
  
  def getRecentStories(self, no_of_stories=10):
    """Used to get the most recent stories in json format {news: [story_1, story_2,..,story_number_of_stories]}"""
    stories_array = []
    for story in self.stories.find().sort('date', 1).limit(no_of_stories): 
      stories_array.append(str(story["_id"]))
    stories = {'news': stories_array, 'timestamp' : time.time()}
    return stories
    
  def getStory(self, story_id):
    """Given the story id gives a story summary and title"""
    try:
      id = objectid.ObjectId(str(story_id))
    except objectid.InvalidId:
      return {'error' : 'Invalid Id'}
    story = self.stories.find_one({'_id':id})  
    if story != None:
      return {'title': story["title"], 'summary': story["summary"], 'wordcloud': story["periods"][-1]["wordcloud"]}
    else:
      return {'error' : 'Story does not exist'}
      
  
  def getStories(self):
    """Used to get all the stories"""
    stories = []
    for story in self.stories.find():
      stories.append(story["title"])
    return stories
    

if __name__ == "__main__":
  d = Database()
  print d.getRecentStories(10)
  #print d.getStory("4eb428e91786f0117a000003")
  print d.getStoriesByTimeStamp()