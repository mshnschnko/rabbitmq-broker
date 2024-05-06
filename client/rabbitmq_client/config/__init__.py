import configparser

app_config = configparser.ConfigParser()
app_config.read('rabbitmq_client/app.ini', 'utf8')

HOST = app_config.get('broker', 'host')
PORT = app_config.getint('broker', 'port')
WAITING_TIME = app_config.getint('broker', 'waiting_time')

SERVER_QUEUE = app_config.get('server', 'queue')

SERVER_ERROR_MESSAGE = app_config.get('error', 'server_error')
ERROR_WINDOW_TITLE = app_config.get('error', 'server_error_title')

LOGGER_NAME = app_config.get('loggers', 'keys')