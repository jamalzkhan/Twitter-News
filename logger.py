import logging

class Logger():
    
  def __init__(self, console_logging=True, file_logging=True, file_name="log.log"):
    
    # Collection of loggers
    self.loggers = {}
    self.console_logging = console_logging
    self.file_logging = file_logging
    self.file_name = file_name
    
    self.format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Console logging options
    self.console = logging.StreamHandler()
    self.console.setLevel(logging.INFO)
    self.console.setFormatter(logging.Formatter(self.format))
  
    if (file_logging and console_logging) or file_logging:
      
      # Adding only file logging
      self.config = logging.basicConfig(format = self.format, filename=self.file_name, filemode='w', level=logging.INFO)
      
    elif console_logging:
      
      # Logging to console if file logging is not present
      self.config = logging.basicConfig(format = self.format, level=logging.INFO)
      
    else:
      
      self.config = None
      
  def addLogger(self, name):
    self.loggers[name] = logging.getLogger(name)
    
    # If we need to log to the console then add the console handler
    if self.console_logging and self.file_logging:
      self.loggers[name].addHandler(self.console)
  
  def info(self, name, message):
    self.loggers[name].info(message)
  
  def error(self, name, message):
    self.loggers[name].error(message)
    
  def warning(self, name, message):
    self.loggers[name].warning(message)
    
  def debug(self, name, message):
    self.loggers[name].debug(message)
  
  
if __name__ == "__main__":
  r = Logger()
  r.addLogger("Rafal")
  r.info("Rafal", "Sam is gay")
 
  
  