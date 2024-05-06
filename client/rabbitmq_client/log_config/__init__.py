import configparser

log_config = configparser.ConfigParser()
log_config.read('rabbitmq_client/app.ini', 'utf8')

FILENAME = eval(log_config.get('handler_logfile', 'args'))[0]
FORMAT = log_config.get('formatter_logformatter', 'format', raw=True)
LEVEL = log_config.get('logger_root', 'level')
FILE_LEVEL = log_config.get('handler_logfile', 'level')
CONSOLE_LEVEL = log_config.get('handler_logconsole', 'level')