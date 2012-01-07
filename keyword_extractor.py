import ConfigParser, json, urllib

class KeywordExtractor:
  
  def __init__(self, logger, limit=3):
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    self.key = config.get('alchemyapi','key')
    self.stream = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords"
    self.apikey_option = 'apikey=' + self.key
    self.output_option = 'outputMode=' + 'json'
    self.keyword_limit_option = 'maxRetrieve={0}'.format(limit)
    self.logger = logger

  def getKeywords(self, story):
    """Gets Keywords given a particular story in JSON format which is then put into a list"""
    # Building Alchemy API call
    call = self.stream +  '?' + self.apikey_option + "&" + 'url=' + story["link_main_story"] + "&" + self.output_option + '&' + self.keyword_limit_option
    data = urllib.urlopen(call)
    try:
      keywords = []
      #Fetching data from Alchemy API
      data = json.loads(data.read())
      keyword_data =  data['keywords']
      
      #We only care about the keywords
      for keyword_entry in keyword_data:
        keywords.append(unicode(keyword_entry['text']))
      return keywords
    except ValueError as strerror:
      logger.error("Error while parsing keywords: {}".format(strerror))
      return []

if __name__ == "__main__":
  k = KeywordExtractor()
