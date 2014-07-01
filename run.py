#!/usr/bin/python
from gevent import monkey
monkey.patch_all()
from app import create_app, socketio

app = create_app(False)

if __name__ == '__main__':
	socketio.run(app,'0.0.0.0',80)
