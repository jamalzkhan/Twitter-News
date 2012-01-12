import time
from flask import Flask, render_template, Response
import db
import datetime

import json
from bson.objectid import ObjectId

app = Flask(__name__)
database = db.Database()

# jsonify hacks

class APIEncoder(json.JSONEncoder): 
  def default(self, obj): 
     if isinstance(obj, (datetime.datetime, datetime.date)): 
         return obj.ctime() 
     elif isinstance(obj, datetime.time): 
         return obj.isoformat() 
     elif isinstance(obj, ObjectId): 
         return str(obj) 
     return json.JSONEncoder.default(self, obj)
    
def jsonify(data):
  return Response(json.dumps(data, cls=APIEncoder, indent = 1), mimetype='application/json')

@app.route("/")
# This is where we need to setup the main UI
def index():
  #For testing purposes, stub
  return render_template('index.html')

@app.route("/specialedition")
# This is the special edition!
def special();
  return render_template('special.html')

@app.route("/story/<int:story_id>")
# This is where we need to setup the story UI. It doesn't have to be an ID, maybe we can use story name.
# But for now I'll leave it as an ID.
def show_story(story_id):
  return "This is story {}".format(story_id)

# API
# The API returns mainly json objects
# If there is an error in your request then the json object with contain an 'error' field with a relevant message

@app.route("/api/news")
def api_main_news():
  """Returns the top news story summaries in the following format {'news':[array_of_stories_as_strings]}"""
  return jsonify(database.getRecentStories(10));

@app.route("/api/news/before/<timestamp>")
def api_main_news_until(timestamp):
  time = float(timestamp)
  return jsonify(database.getStoriesAddedBeforeTimestamp(time))

@app.route("/api/news/after/<timestamp>")
def api_main_news_since(timestamp):
  time = float(timestamp)
  return jsonify(database.getStoriesAddedAfterTimestamp(time))

@app.route("/api/story/<story_id>")
def api_story(story_id):
  story = database.getStory(story_id)
  if "error" in story:
    return jsonify(story)
  else:
    story['wordcloud'] = prepareWordCloud(story["wordcloud"])
    return jsonify(story)
    

def prepareWordCloud(cloud):
  if len(cloud) == 0:
    return {}
  cloud = cloud.copy()
  min_v = float(cloud[min(cloud, key=cloud.get)])
  for w in cloud:
    cloud[w] = cloud[w]/min_v
  return cloud

if __name__ == "__main__":
  # Setting up debugging environment (server reloads itself and provides better error messages)
  app.debug = True
  # app.run()
  
  # This is, so that the website is externally visible
  app.run(host='0.0.0.0')
