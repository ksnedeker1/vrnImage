import pika
import requests
import json


def call_metrics_microservice(image_path1, image_path2):
    """
    Calls the metrics microservice with the paths of the original and compressed images.
    Returns MSE, PSNR.
    """
    res = [None]

    def callback(ch, method, properties, body):
        res[0] = body.decode()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        connection.close()

    # POST request to /enqueue
    url_enqueue = 'http://localhost:5000/enqueue'
    headers = {'Content-Type': 'application/json'}
    data = {
        'image_path1': image_path1,
        'image_path2': image_path2
    }
    response_enqueue = requests.post(url_enqueue, headers=headers, data=json.dumps(data))
    # Listen to results MQ after POST request sent
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='results_queue', durable=True)
    channel.basic_consume(queue='results_queue', on_message_callback=callback)
    channel.start_consuming()
    return res[0]
