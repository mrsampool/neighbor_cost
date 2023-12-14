import pika
from components.event_manager.event_body import EventBody


class EventManager:
    def __init__(self, host: str, queue_name: str):
        self.host = host
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue_name)
        self.queue_name = queue_name

    def publish(self, body: EventBody):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=body.to_json().encode('utf-8')
        )

    def consume(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()


"""
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = conn.channel()
    channel.queue_declare(queue="zhvi-collection")

    channel.basic_publish(
        exchange="",
        routing_key="zhvi_collection",
        body=json.dumps({
            "my message": "hi!",
        }).encode('utf-8')
    )
    
"""
