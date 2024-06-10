import pika
import uuid

import pika.exceptions
from proto import Request, Response
from config import Config
from log_config import LogConfig
from logger import get_logger


log_config = LogConfig()
logger = get_logger(log_config.logger_name)

class Interacter:
    def __init__(self, host: str | None = None, port: str | int | None = None) -> None:
        self.config = Config()
        self.connection = None


    def connect(self, host: str | None = None, port: str | int | None = None) -> None:
        host = host if host else self.config.host
        port = port if port else self.config.port

        logger.info("Connection opening...")

        self.connection = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        logger.info("Connection opened")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config.server_queue)
        logger.info(f"Server queue was declarated")
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        logger.info(f"Client queue was declarated: {self.callback_queue}")

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.callback,
            auto_ack=True)
        
        logger.info(f"Consuming queue: {self.callback_queue}")

        self.response = None
        self.corr_id = None


    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")
        self.connection = None
        self.response = None
        self.corr_id = None


    def callback(self, ch, method, properties, body):
        response = Response()
        response.ParseFromString(body)
        if self.corr_id == properties.correlation_id:
            logger.info(f"Response was received. Response id: {self.corr_id}. Content: {response.res}")
            self.response = response.res


    def call(self, n: int) -> int | None:
        self.response = None
        self.corr_id = str(uuid.uuid4())

        request = Request()
        request.id = self.corr_id
        request.req = n
        serialized_message = request.SerializeToString()

        logger.info(f"Sending request. Server queue: {self.config.server_queue}. Client queue: {self.callback_queue}. Request id: {request.id}. Content: {request.req}")

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.config.server_queue,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=serialized_message)
            
            logger.info(f"Request was sent")

            try:
                waiting_time = int(self.config.waiting_time)
                if waiting_time < 0: waiting_time = None
            except:
                waiting_time = None
            self.connection.process_data_events(time_limit=waiting_time)
        except pika.exceptions.AMQPError as e:
            logger.error(f"Error with message publishing: {e}")
        
        return int(self.response)


    def __del__(self) -> None:
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")
