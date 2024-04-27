import pika
import uuid

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
        # self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        # self.channel.queue_declare(queue=SENDER_QUEUE)
        
    # def send_message(self, message: str) -> None:
    #     print(type(message))
    #     self.channel.basic_publish(exchange='',
    #                         routing_key=SENDER_QUEUE,
    #                         body=message)
    #     print(f" [x] Sent '{message}'")
    #     self.cons()

    def callback(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, n: int):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=SENDER_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events(time_limit=3)
        print(f'[x] Received: {int(self.response)}')
        return int(self.response)

    # def cons(self):
    #     for method_frame, properties, body in self.channel.consume(queue=SENDER_QUEUE, auto_ack=True, inactivity_timeout=3):
    #         if method_frame:
    #             self.callback(self.channel, method_frame, properties, body)
    #             return body
    #         else:
    #             print("No message received within inactivity timeout")
    #             break
        

    # @staticmethod
    # def callback(ch, method, properties, body) -> None:
    #     print(f" [x] Received {body}")

    def __del__(self) -> None:
        self.connection.close()
        print(" [x] Connection closed")
