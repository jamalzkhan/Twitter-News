import logger

class Log:
  
  def __init__(self, name, logger):
    self.name = name
    self.logger = logger
    
    logger.addLogger(name)
    
  def info(self, message):
    self.logger.info(self.name, message)
    
  def error(self, message):
    self.logger.error(self.name, message)
    
  def warning(self, message):
    self.logger.warning(self.name, message)
    
  def debug(self):
    self.logger.debug(self.name, message)