import requests
import json
import os
import pika


def callback(ch, method, body):
    print(f"Received Result: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    connection.close()


# Get abs paths of images
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path1 = os.path.join(current_dir, '../images', 'ireland1.jpg')
image_path2 = os.path.join(current_dir, '../images', 'ireland1delete.jpg')

# Send POST request to /enqueue
url_enqueue = 'http://localhost:5000/enqueue'
headers = {'Content-Type': 'application/json'}
data = {
    'image_path1': image_path1,
    'image_path2': image_path2
}
response_enqueue = requests.post(url_enqueue, headers=headers, data=json.dumps(data))
# remove me
print(response_enqueue.json())

# Listen to results MQ after POST request sent
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='results_queue', durable=True)

channel.basic_consume(queue='results_queue', on_message_callback=callback)
channel.start_consuming()
