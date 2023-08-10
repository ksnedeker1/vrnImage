import pika
import cv2
import numpy as np


def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


def calculate_mse(image1, image2):
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1] * image1.shape[2])
    return err


def calculate_psnr(image1, image2):
    mse = calculate_mse(image1, image2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def callback(ch, method, properties, body):
    image_path1, image_path2 = body.decode().split(',')

    # Load images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Resize the images to be the same size
    if image1.shape != image2.shape:
        image1 = resize_image(image1, width=image2.shape[1], height=image2.shape[0])

    mse = calculate_mse(image1, image2)
    psnr = calculate_psnr(image1, image2)

    print(f"Processed images: {image_path1} and {image_path2}")
    print(f"MSE={mse}, PSNR={psnr}")

    result_message = f"{image_path1},{image_path2},{mse},{psnr}"
    channel.basic_publish(
        exchange='',
        routing_key='results_queue',
        body=result_message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
channel.queue_declare(queue='results_queue', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()