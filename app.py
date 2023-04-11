from flask import Flask, render_template, request
from gevent import monkey
# from geventwebsocket.handler import WebSocketHandler
# from geventwebsocket.logging import create_logger
# from gevent.pywsgi import WSGIServer
from flask_socketio import SocketIO, send, emit
import logging


monkey.patch_all()

app = Flask(__name__)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, logger=True, engineio_logger=True)
socketio = SocketIO(app, async_mode='gevent')
# socketio = SocketIO(app, async_mode='gevent',cors_allowed_origins="*")
# socketio = SocketIO(app, async_mode='gevent', transport='websocket')
# socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True)
# socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    app.logger.info('Client connected')

@socketio.on('message')
def handle_message(message):
    app.logger.debug('Received message: ' + message)
    send(message, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    app.logger.info('Client disconnected')

@socketio.on('my event')
def handle_my_custom_event(json):
    app.logger.debug('Received event: ' + str(json))
    emit('my response', json, broadcast=True)

@socketio.on_error_default
def default_error_handler(e):
    app.logger.info('An error occurred:', e)

if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()
    # socketio.run(app, server=http_server)
    socketio.run(app)
