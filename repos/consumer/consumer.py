import pika
import os
import logging
import sys
import argparse
import time
import json
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv
from argparse import RawTextHelpFormatter
from time import sleep


app = Flask(__name__)
is_connected = False
lock = threading.Lock()

logginginst = None
rabbit_server = ""
rabbit_port = ""
rabbit_user = ""
rabbit_password = ""


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print("date: " + str(json.loads(body)["date"]))
    print("message: " + str(json.loads(body)["message"]))
    print("======")
    logginginst.info('Message has been received %s', body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def connect_to_rabbitmq():
    global is_connected
    credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
    parameters = pika.ConnectionParameters(rabbit_server,
                                           int(rabbit_port),
                                           '/',
                                           credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        is_connected = True
        channel = connection.channel()

        channel.queue_declare('pc')
        channel.basic_consume('pc', on_message)

        channel.start_consuming()
    except Exception:
        is_connected = False
        channel.stop_consuming()
        connection.close()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint that returns the connection status"""
    with lock:
        status = is_connected
    if status:
        return jsonify({'status': 'ok', 'connected': True}), 200
    else:
        return jsonify({'status': 'error', 'connected': False}), 500



if __name__ == '__main__':
    logginginst
    logging.basicConfig(level=logging.INFO)
    logginginst = logging.getLogger(__name__)
    load_dotenv()
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Run consumer.py',
                                     epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.')
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

    consumer_thread = threading.Thread(target=connect_to_rabbitmq)
    consumer_thread.daemon = True
    consumer_thread.start()

    app.run(host='0.0.0.0', port=5000)
