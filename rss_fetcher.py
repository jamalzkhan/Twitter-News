import feedparser, pymongo, json, hashlib, bson, threading, time
from dateutil import parser    # For easily parsing strings to Date
from BeautifulSoup import BeautifulSoup # For Parsing descriptions
import keyword_extractor
import shared
import helpers

class RssFetcher(threading.Thread):
  def __init__(self, log=None, rss="http://news.google.com/?output=rss", sleeptime=500):
    threading.Thread.__init__(self)
    self.extractor = keyword_extractor.KeywordExtractor(log)
    self.rss_link = rss
    self.sleeptime = sleeptime
    self.log = log
  
  def run(self):
    while 1:
      shared.event.clear()
      self.getNews()
      # We got the news, so we allow the tweet thread to work 
      shared.event.set()
      
      # Sleep for 5 minutes
      self.log.info("Going to sleep for {0}.".format(self.sleeptime))
      time.sleep(self.sleeptime)
      self.log.info("Waking up.")
      
      shared.flag = True
  
  @staticmethod
  def gNews_title_fix(title):
    """Gets rid of the final hyphen of the Google News titles 
       from the google news api"""
    dashOccurence = (len(title) - 1) - title[::-1].index('-')
    return title[0:dashOccurence]
  
  @staticmethod
  def gNews_get_link_main_story(link):
    """Get the news URL from a weirdly crafted google news url"""
    return link[link.find("&url=")+len("&url="):]
  
  @staticmethod
  def gNews_get_summary(description):
    return BeautifulSoup(description).findAll('div',{'class':'lh'})[0].findAll('font',{'size':'-1'})[1].contents[0]
  
  @staticmethod
  def gNews_get_link(description):
    return BeautifulSoup(description).findAll('div',{'class':'lh'})[0].findAll('font',{'size':'-1'})[-1].a['href']
  
  def getNews(self):
    """Download news stories and put them in the shared list"""
    self.log.info("Fetching news feed from {0}.".format(self.rss_link))
    feed = feedparser.parse(self.rss_link)
    self.news_stories = []
    
    for entry in feed["items"]:
      self.log.info("Parsing story {0}.".format( helpers.toAscii(entry["title"])) )
      news_story = {}
      news_story["title"] = RssFetcher.gNews_title_fix(entry["title"])
      news_story["link_main_story"] = RssFetcher.gNews_get_link_main_story(entry["link"])
      news_story["link"] = RssFetcher.gNews_get_link(entry["description"])
      news_story["summary"] = RssFetcher.gNews_get_summary(entry["description"])
      news_story["date"] = parser.parse(entry["updated"])
      news_story["keywords"] = self.extractor.getKeywordsByURL(news_story["link_main_story"])
      self.news_stories.append(news_story)
    
    self.log.info("Putting a new set of stories into the shared list.")
    shared.stories = self.news_stories
  

if __name__ == "__main__":
  r = RssFetcher()
  r.getNews()
