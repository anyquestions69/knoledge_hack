import json
import uuid
import pika
import time
import Tyrenko

print('STARTED WORKER 1')

connection = pika.BlockingConnection(
pika.ConnectionParameters(host='rabbitmq'))
 
channel = connection.channel()

channel.queue_declare(queue='pupupu')


def on_request(ch, method, props, body):
   
    text = json.loads(body.decode('utf-8'))
    print(text)
    response = Tyrenko.determined_text_to_title(text.title, text.text)
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                        props.correlation_id),
                    body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

consumer_tag = uuid.uuid1().hex
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='pupupu',consumer_tag=consumer_tag, on_message_callback=on_request)

print(" [x] Awaiting RPC requests", consumer_tag)
channel.start_consuming()