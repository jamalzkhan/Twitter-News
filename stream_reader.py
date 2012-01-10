import pycurl, json, pymongo, ConfigParser, bson, hashlib, threading, itertools, time

import mongo_connector
import shared
import unicodedata
from dateutil import parser


class StreamReader(threading.Thread):

  def __init__(self,log):
    threading.Thread.__init__(self)
    self.tweet_collection = mongo_connector.MongoConnector().getCol("tweets")

    config = ConfigParser.RawConfigParser()
    config.read('config.conf')

    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    
    self.log = log

  def run(self):
    while 1:
      shared.event.wait()
      self.getTweetsBySubject(list(itertools.chain.from_iterable(map(lambda a : a["keywords"], shared.stories))),
                              self.receive_and_write_to_Mongo)
      shared.flag = False;
  
  def getTweetsBySubject(self, subjects, onwrite):
    
    stream_url  = "https://stream.twitter.com/1/statuses/filter.json"
    self.log.info(u"Getting tweets for keywords:{}".format(",".join(subjects)))
    post_data = "track=" + ",".join(subjects)
    post_data = unicodedata.normalize('NFKD', post_data).encode('ascii','ignore')

    conn = self.openStream(stream_url, onwrite)
    conn.setopt(pycurl.POST, 1)
    conn.setopt(pycurl.POSTFIELDS, post_data)
    
    # Stream until I need to change the keyword list
    try:
      conn.perform()
    except Exception:
      self.log.info(unicode("Story list updated. Restarting stream."))
      conn.close()
  
  def openStream(self, stream, write_function):
    conn = pycurl.Curl()
    conn.setopt(pycurl.USERPWD, "%s:%s" % (self.twitter_username, self.twitter_password))
    conn.setopt(pycurl.URL, stream)
    conn.setopt(pycurl.WRITEFUNCTION, write_function)
    return conn
  
  def on_receive(self, data):
    print json.loads(data)
  
  def receive_and_write_to_Mongo(self, data):    
    while(data.find("many requests") > -1 ):
      self.log.error(unicode("Twitter is throttling us... Waiting 30 seconds"))
      time.sleep(30)
      self.log.error(unicode("Finished waiting"))
      
    try:
      # Means we need to restart with new set of keywords
      if shared.flag:
        # This will get out of the pycurl thread, it will cause
        # an exception
        return -1

      data = json.loads(data)
      data["_id"] = bson.objectid.ObjectId(hashlib.md5(str(data["id"])).hexdigest()[:24])
      data["created_at"] =  parser.parse(data["created_at"])
      if( type( data["retweet_count"]) != int ):
        data["retweet_count"] = 100 # Twitter gives us string '100+'
        
      self.tweet_collection.insert(data)

    except ValueError:
      self.log.info(unicode("Tweet had an error. Not adding to DB."))


def main():
  t = StreamReader()
  t.getTweetsBySubject(['libya,gaddafi'], t.receive_and_write_to_Mongo)

if __name__ == "__main__":
  main()
