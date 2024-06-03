import configparser

class Config:
    __instance: 'Config' = None

    def __new__(cls) -> 'Config':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        self.read_config()

    def read_config(self) -> None:
        app_config = configparser.ConfigParser()
        app_config.read('rabbitmq_client/app.ini', 'utf8')

        self.host = app_config.get('broker', 'host')
        self.port = app_config.get('broker', 'port')
        self.waiting_time = app_config.get('broker', 'waiting_time')
        self.server_queue = app_config.get('server', 'queue')
