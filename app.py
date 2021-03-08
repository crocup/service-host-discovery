"""
Сервис для обнаружения хостов в сети
Dmitry Livanov, 2021
ver 0.0.2
"""
from flask import Flask, request, abort, jsonify
import config
from task import get_hosts
from rq import Queue
from worker import conn

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
q = Queue(connection=conn)


@app.route('/api/v1/discovery/get', methods=['POST'])
def get_task():
    """

    :return:
    """
    if not request.json or not 'host' in request.json:
        abort(400)
    data = request.json
    q.enqueue_call(
        func=get_hosts, args=(data['host'],), result_ttl=500
    )
    return jsonify({"result": "OK"})


if __name__ == '__main__':
    app.run(port=9001)