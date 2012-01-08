from topia.termextract import extract

class KeywordExtractor:
  def __init__(self, logger, limit=3):
    self.logger = logger
    self.keyword_limit = limit
    self.extractor = extract.TermExtractor()

  def getKeywords(self, story):
    return map(lambda a : a[0], self.extractor(story["title"]))
    
if __name__ == "__main__":
  k = KeywordExtractor()
