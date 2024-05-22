import configparser

log_config = configparser.ConfigParser()
log_config.read('rabbitmq_client/logger.ini', 'utf8')

LOGGER_NAME = log_config.get('loggers', 'keys')
FILENAME = log_config.get('handler_logfile', 'file')
FORMAT = log_config.get('formatter_logformatter', 'format', raw=True)
LEVEL = log_config.get('logger_root', 'level')
FILE_LEVEL = log_config.get('handler_logfile', 'level')
CONSOLE_LEVEL = log_config.get('handler_logconsole', 'level')