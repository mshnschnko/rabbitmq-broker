import pika

from proto import Request, Response
from config import HOST, PORT, RECEIVER_QUEUE, EXCHANGE_NAME, EXCHANGE_TYPE

class Server:
    def __init__(self, host: str = HOST, port: str | int = PORT) -> None:
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RECEIVER_QUEUE)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=RECEIVER_QUEUE, on_message_callback=self.callback)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
        

    @staticmethod
    def callback(ch, method, properties, body) -> None:

        request = Request()
        request.ParseFromString(body)

        response = Response()
        response.id = request.id
        response.res = 2 * request.req

        serialized_response = response.SerializeToString()

        ch.basic_publish(exchange='',
                        routing_key=properties.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            properties.correlation_id),
                        body=serialized_response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __del__(self) -> None:
        self.connection.close()
        print(" [x] Connection closed")
