import rss_fetcher
import stream_reader
import analysis
import log
import logger
   
class Twitinfo:
  
  def __init__(self):
    
    self.logger = logger.Logger(console_logging=True, file_logging=True)
    
    self.r_log = log.Log("RSS Fetcher   ", self.logger)
    self.s_log = log.Log("Stream Fetcher", self.logger)
    self.a_log = log.Log("Analysis      ", self.logger)
    
    
    self.r = rss_fetcher.RssFetcher(log=self.r_log)
    self.s = stream_reader.StreamReader(log=self.s_log)
    self.a = analysis.Analysis(log=self.a_log)
    
    
  def start(self):
    
    self.r.start()
    self.s.start()
    self.a.start()
  
if __name__ == "__main__":
  Twitinfo().start()
