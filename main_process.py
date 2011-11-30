import rss_fetcher
import stream_reader
import analysis
import loggers.log as log
import loggers.logger as logger
   
class Twitinfo:
  
  def __init__(self):
    
    main_logger = logger.Logger()
    
    r_log = log.Log("RSS Fetcher", main_logger)
    s_log = log.Log("Tweet Fetcher", main_logger)
    a_log = log.Log("Analysis", main_logger)
    
    
    self.r = rss_fetcher.RssFetcher(r_log)
    self.s = stream_reader.StreamReader(s_log)
    self.a = analysis.Analysis(a_log)
    
    
  def start(self):
    
    self.r.start()
    self.s.start()
    self.a.start()
  
if __name__ == "__main__":
  Twitinfo().start()
