import pika
from config import HOST, PORT, RECEIVER_QUEUE

class Receiver:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        self.channel.queue_declare(queue=RECEIVER_QUEUE)

        self.channel.basic_consume(queue=RECEIVER_QUEUE, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body) -> None:
        print(f" [x] Received {body}")

if __name__ == '__main__':
    receiver = Receiver()