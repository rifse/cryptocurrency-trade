# from enum import Enum

# ALL LOGGERS
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

class Settings:
    modules = {'main': 'DEBUG', 
               'bitstamp': 'DEBUG', 
               'bitfinex': 'DEBUG', 
               'binance': 'DEBUG'}
    settings = {'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'verbose': {
                        'format': '%(levelname)s %(asctime)s %(name)s %(message)s'}},
                'handlers': {
                    'console': {
                        'level':'DEBUG',
                        'class':'logging.StreamHandler',
                        'formatter': 'verbose'}},
                'loggers': {}}

    @classmethod        
    def load(cls):
        for module in cls.modules:  # .keys()
            file_handler = f'file_{module}'
            file_name = f'../logs/{module}.log'
            level = cls.modules[module]
            handler = {'level': 'INFO',  # level,
                       'class':'logging.FileHandler',
                       'formatter': 'verbose',
                       'filename': file_name,}
            cls.settings['handlers'].update({file_handler: handler})

            logger = {'handlers': ['console', file_handler],
                      'propagate': True,
                      'level': level}
            cls.settings['loggers'].update({module: logger})
        return cls.settings
