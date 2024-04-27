import configparser

app_config = configparser.ConfigParser()
app_config.read('rabbitmq_server/server.ini', 'utf8')

HOST = app_config.get('broker', 'host')
PORT = app_config.getint('broker', 'port')
EXCHANGE_NAME = app_config.get('broker', 'exchange_name')
EXCHANGE_TYPE = app_config.get('broker', 'exchange_type')
HOST = app_config.get('broker', 'host')

RECEIVER_QUEUE = app_config.get('receiver', 'queue')