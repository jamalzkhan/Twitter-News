import ConfigParser, json, urllib, urllib2, itertools

class KeywordExtractor:
  
  def __init__(self, logger, limit=10):
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    self.url = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords"
    self.request_data = {}
    self.request_data["apikey"] = config.get('alchemyapi','key')
    self.request_data["outputMode"] = 'json'
    self.request_data["maxRetrieve"] = limit
    self.request_data["sourceText"] = 'cleaned_or_raw'
    self.logger = logger
    self.blacklist = [line.strip() for line in open('keyword_filter_list.txt')]

  def getKeywords(self, story):
    """Gets Keywords given a particular story in JSON format which is then put into a list"""
    request_data = self.request_data.copy()
    request_data["url"] = story["link_main_story"]
    r = urllib2.Request(url=self.url)
    r.add_data(urllib.urlencode(request_data))
    response = urllib2.urlopen(r)
    try:
      #Fetching data from Alchemy API
      data = json.loads(response.read())
      if (data["status"] == "OK"):
        #We only care about the keywords
        keywords = []
        for keyword_entry in data['keywords']:
          if (float(keyword_entry["relevance"]) >= 0.7):
            keyword = keyword_entry['text'].lower()
            keyword_words = keyword.split()
            keyword_words = itertools.ifilterfalse(lambda x: x in self.blacklist,keyword_words)
            keyword = unicode(" ").join(keyword_words)
            keywords.append(keyword)
        return keywords
      else:
        self.logger.error("Error while parsing the response from Alchemy API. Response: {}".format(data))
        return []

    except ValueError as strerror:
      self.logger.error("Error while parsing keywords: {}".format(strerror))
      return []
    except KeyError as strerror:
      self.logger.error("Problem with key: {}".format(strerror))
      return []

if __name__ == "__main__":
  k = KeywordExtractor()
