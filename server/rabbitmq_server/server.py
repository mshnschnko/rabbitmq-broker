import pika
import pika.exceptions

from proto import Request, Response
from config import HOST, PORT, RECEIVER_QUEUE, EXCHANGE_NAME, EXCHANGE_TYPE, LOGGER_NAME
from logger import get_logger

logger = get_logger(LOGGER_NAME)

class Server:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        logger.info("Server starting...")

        self.connection = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        logger.info("Connection opened")
        
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RECEIVER_QUEUE)
        logger.info(f"Queue was declarated: {RECEIVER_QUEUE}")
        self.channel.basic_qos(prefetch_count=1)
        
        self.channel.basic_consume(queue=RECEIVER_QUEUE, on_message_callback=self.callback)
        logger.info("Awaiting requests...")
        self.channel.start_consuming()
        

    @staticmethod
    def callback(ch, method, properties, body) -> None:
        request = Request()
        request.ParseFromString(body)

        logger.info(f"Request was received. From: {request.id}. Content: {request.req}")

        response = Response()
        response.id = request.id

        response.res = 2 * request.req

        serialized_response = response.SerializeToString()

        try:
            ch.basic_publish(exchange='',
                            routing_key=properties.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                properties.correlation_id),
                            body=serialized_response)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Response was sent. Client queue: {properties.reply_to}. To: {response.id}. Content: {response.res}")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Error with message publishing: {e}")

    def __del__(self) -> None:
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")
