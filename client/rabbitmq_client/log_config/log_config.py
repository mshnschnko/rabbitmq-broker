import configparser

class LogConfig:
    __instance: 'LogConfig' = None

    def __new__(cls) -> 'LogConfig':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        self.read_config()

    def read_config(self) -> None:
        log_config = configparser.ConfigParser()
        log_config.read('rabbitmq_client/logger.ini', 'utf8')

        self.logger_name = log_config.get('loggers', 'keys')
        self.filename = log_config.get('handler_logfile', 'file')
        self.format = log_config.get('formatter_logformatter', 'format', raw=True)
        self.level = log_config.get('logger_root', 'level')
        self.file_level = log_config.get('handler_logfile', 'level')
        self.console_level = log_config.get('handler_logconsole', 'level')

    def update_config_file(self) -> None:
        log_config = configparser.ConfigParser()
        log_config.read('rabbitmq_client/logger.ini', 'utf8')

        log_config.set('handler_logfile', 'file', self.filename)
        log_config.set('logger_root', 'level', self.level)

        with open('rabbitmq_client/logger.ini', 'w', encoding='utf8') as log_config_file:
            log_config.write(log_config_file)