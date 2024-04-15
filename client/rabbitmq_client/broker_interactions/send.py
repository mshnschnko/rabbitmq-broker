import pika
from config import HOST, PORT, SENDER_QUEUE

class Sender:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=SENDER_QUEUE)
        
    def send_message(self, message: str) -> None:
        print(type(message))
        self.channel.basic_publish(exchange='',
                            routing_key=SENDER_QUEUE,
                            body=message)
        print(f" [x] Sent '{message}'")

    def __del__(self) -> None:
        self.connection.close()
