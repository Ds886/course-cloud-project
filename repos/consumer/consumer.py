import pika
import logging
import sys
import argparse
import time
from argparse import RawTextHelpFormatter
from time import sleep


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print("======")
    LOG.info('Message has been received %s', body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Run consumer.py',
                                     epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.')
    rabbit_server = ""
    rabbit_port = ""
    rabbit_user = ""
    rabbit_password = ""

    args = parser.parse_args()
    if os.getenv("RABBIT_HOST") is not None:
        rabbit_server = os.getenv("RABBIT_HOST")
    else:
        if args.server is not None:
            rabbit_server = args.server
        else:
            print("Missing required argument: -s/--server")
            sys.exit(1)

    if os.getenv("RABBIT_PORT") is not None:
        rabbit_port = os.getenv("RABBIT_PORT")
    else:
        if args.port is not None:
            rabbit_port = args.port
        else:
            print("Missing required argument: -p/--port")
            sys.exit(1)

    if os.getenv("RABBIT_PASSWORD") is not None:
        rabbit_password = os.getenv("RABBIT_PASSWORD")
    else:
        print("Missing required parameter RABBIT_PASSWORD")
        sys.exit(1)

    if os.getenv("RABBIT_USER") is not None:
        rabbit_user = os.getenv("RABBIT_USER")
    else:
        print("Missing required parameter RABBIT_USER")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
    parameters = pika.ConnectionParameters(rabbit_server,
                                           int(rabbit_port),
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare('pc')
    channel.basic_consume(on_message, 'pc')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
