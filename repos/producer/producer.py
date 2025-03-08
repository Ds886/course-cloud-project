import pika
import logging
import sys
import argparse
import os
import json
import datetime
from argparse import RawTextHelpFormatter
from time import sleep
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    examples = sys.argv[0] + " -p 5672 -s rabbitmq -m 'Hello' "
    parser = argparse.ArgumentParser(
                                     formatter_class=RawTextHelpFormatter,
                                     description='Run producer.py',
                                     epilog=examples
                                 )
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.', required=False)
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.', required=False)
    parser.add_argument('-m', '--message', action='store', dest='message', help='The message to send', required=False, default='Hello')
    parser.add_argument('-r', '--repeat', action='store', dest='repeat', help='Number of times to repeat the message', required=False, default='30')

    rabbit_server = ""
    rabbit_port = ""
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

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    credentials = pika.PlainCredentials('user', 'test')
    parameters = pika.ConnectionParameters(rabbit_server,
                                           int(rabbit_port),
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    q = channel.queue_declare('pc')
    q_name = q.method.queue

    # Turn on delivery confirmations
    channel.confirm_delivery()

    while True:
        curr_obj = {
            "date": str(datetime.datetime.now()),
            "message": args.message
        }
        try:
            if channel.basic_publish('', q_name, json.dumps(curr_obj)):
                LOG.info('Message has been delivered')
        except Exception as e:
            LOG.warning('Message NOT delivered' + e)

        sleep(20)

    connection.close()
