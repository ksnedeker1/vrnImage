from flask import Flask, request, jsonify
import pika

app = Flask(__name__)


@app.route('/enqueue', methods=['POST'])
def enqueue_image_quality_metrics():
    data = request.get_json()
    image_path1 = data['image_path1']
    image_path2 = data['image_path2']

    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='task_queue', durable=True)

    # Send the work item to the queue
    message = f"{image_path1},{image_path2}"
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    connection.close()

    return jsonify({'status': 'Task enqueued'})


# @app.route('/purge', methods=['POST'])
# def purge_queue():
#     # Connect to RabbitMQ server
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     channel.queue_purge(queue='task_queue')
#
#     connection.close()
#
#     return jsonify({'status': 'Queue purged'})
#

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
