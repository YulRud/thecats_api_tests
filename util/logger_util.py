import logging
import sys

class Logger():  
    _logger_map = {}

    def __init__(self, name=__name__):    

        if name in Logger._logger_map:
             self.logger = Logger._logger_map[name]
        else:    
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.INFO)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler('test.log')
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(name)s (line: %(lineno)d) -  %(message)s')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            Logger._logger_map[name] = self.logger
                
        self.logger.info('Logger initialized')

    def get_logger(self):
        return self.logger
    