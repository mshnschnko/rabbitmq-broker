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

        self.username = app_config.get('credentials', 'username')
        self.password = app_config.get('credentials', 'password')

    def update_config_file(self) -> None:
        app_config = configparser.ConfigParser()
        app_config.read('rabbitmq_client/app.ini', 'utf8')

        app_config.set('broker', 'host', self.host)
        app_config.set('broker', 'port', self.port)
        app_config.set('broker', 'waiting_time', self.waiting_time)
        app_config.set('server', 'queue', self.server_queue)
        app_config.set('credentials', 'username', self.username)
        app_config.set('credentials', 'password', self.password)

        with open('rabbitmq_client/app.ini', 'w', encoding='utf8') as app_config_file:
            app_config.write(app_config_file)