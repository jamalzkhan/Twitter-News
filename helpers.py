import unicodedata

def toAscii(text):
  return unicodedata.normalize('NFKD', text).encode('ascii','ignore')
  
def extractTweetIds(data):
  return map(lambda x : x['id'], data)