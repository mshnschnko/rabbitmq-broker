import pika
from config import HOST, PORT, RECEIVER_QUEUE, EXCHANGE_NAME, EXCHANGE_TYPE

class Interacter:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RECEIVER_QUEUE)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=RECEIVER_QUEUE, on_message_callback=self.callback)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
        # self.channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)
        
        # self.channel.queue_declare(queue=SENDER_QUEUE)
        
    # def send_message(self, message: str) -> None:
    #     print(type(message))
    #     self.channel.basic_publish(exchange='',
    #                         routing_key=SENDER_QUEUE,
    #                         body=message)
    #     print(f" [x] Sent '{message}'")
    #     self.cons()

    # def cons(self):
    #     for method_frame, properties, body in self.channel.consume(queue=SENDER_QUEUE, auto_ack=True, inactivity_timeout=3):
    #         if method_frame:
    #             self.callback(self.channel, method_frame, properties, body)
    #             return body
    #         else:
    #             print("No message received within inactivity timeout")
    #             break
        

    @staticmethod
    def callback(ch, method, properties, body) -> None:
        n = int(body)

        response = 2*n

        ch.basic_publish(exchange='',
                        routing_key=properties.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            properties.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __del__(self) -> None:
        self.connection.close()
        print(" [x] Connection closed")
