import pika
import uuid

from proto import Request, Response
from config import HOST, PORT, SENDER_QUEUE

class Interacter:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.callback,
            auto_ack=True)
        
        self.response = None
        self.corr_id = None


    def callback(self, ch, method, properties, body):
        response = Response()
        response.ParseFromString(body)
        if self.corr_id == properties.correlation_id:
            self.response = response.res


    def call(self, n: int):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = Request()
        message.id = self.corr_id
        message.req = n
        serialized_message = message.SerializeToString()

        self.channel.basic_publish(
            exchange='',
            routing_key=SENDER_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=serialized_message)
        
        while self.response is None:
            self.connection.process_data_events(time_limit=3)
        return int(self.response)


    def __del__(self) -> None:
        self.connection.close()
        print(" [x] Connection closed")
