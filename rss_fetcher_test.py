import rss_fetcher  
import loggers.log as log
import loggers.logger as logger
import unittest


class RssFetcherTest(unittest.TestCase):

  def setUp (self, rss_file="dummy_rss.rss", rss_url=None):
    
    self.rss_file = rss_file
    self.main_logger = logger.Logger()
    self.r_log = log.Log("RSS Test Fetcher", self.main_logger)
    
    
    f = open(self.rss_file, 'r+')
    rss = f.read()
    # print rss
    f.close()
  
    self.rss = rss
  
    self.rss_fetcher = rss_fetcher.RssFetcher(rss=self.rss, log=self.r_log)
      
  def test_rss_is_broken_url(self):
    """ Test to see what happens if the RSS Feed that is passed is broken"""
    self.rss_fetcher.rss_link = "http://thisisfake.com"
    self.rss_fetcher.getNews()
    print self.rss_fetcher.news_stories
    self.assertTrue(len(self.rss_fetcher.news_stories) == 0)
    
  def test_rss_returns_correct_format(self):
    """Test to see that given a dummy feed we get the correct stories"""
    self.rss_fetcher.getNews()
    stories = self.rss_fetcher.news_stories  
    
    # Various checks for the dummy rss feed, whose values are known
    
    self.assertTrue(len(stories) == 2)
    
  
    
if __name__ == "__main__":
  print "Starting Unit Testing for RSS Fetcher Thread"
  unittest.main()
  