import time
from flask import Flask, jsonify, render_template
import db

app = Flask(__name__)
database = db.Database()

@app.route("/")
# This is where we need to setup the main UI
def index():
  #For testing purposes, stub
  return render_template('index.html')

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

@app.route("/api/news/<int:timestamp>")
def api_main_news_since(timestamp):
  return jsonify({'news': [0], 'timestamp': time.time()})

@app.route("/api/story/<story_id>")
def api_story(story_id):
  story = database.getStory(story_id)
  if "error" in story:
    return jsonify(story)
  else:
    title = "News Story {}".format(story["title"])
    return jsonify({'title': title, 'summary': story["summary"]})

if __name__ == "__main__":
  # Setting up debugging environment (server reloads itself and provides better error messages)
  app.debug = True
  app.run()
  
  # This is, so that the website is externally visible
  #app.run(host='0.0.0.0')
