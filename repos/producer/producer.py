import pika
import logging
import sys
import argparse
import os
import json
import datetime
import threading
from argparse import RawTextHelpFormatter
from time import sleep
from dotenv import load_dotenv
from flask import Flask, jsonify


app = Flask(__name__)
is_connected = False
lock = threading.Lock()

logginginst = None
rabbit_server = ""
rabbit_port = ""
rabbit_user = ""
rabbit_password = ""


def connect_to_rabbitmq():
    global is_connected
    credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
    parameters = pika.ConnectionParameters(rabbit_server,
                                           int(rabbit_port),
                                           '/',
                                           credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        is_connected = True
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
                channel.basic_publish('', q_name, json.dumps(curr_obj))
                logginginst.info('Message has been delivered')

            except Exception:
                logginginst.warning('Message NOT delivered' + e)
            sleep(20)

    except Exception:
        is_connected = False
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
    logginginst = logging.getLogger(__name__)

    consumer_thread = threading.Thread(target=connect_to_rabbitmq)
    consumer_thread.daemon = True
    consumer_thread.start()

    app.run(host='0.0.0.0', port=5000)
