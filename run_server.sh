#!/bin/bash

HOST=192.168.0.9
PORT=5000

export FLASK_APP=app
export FLASK_ENV=debug
export FLASK_DEBUG=1
rm -rf app.egg-info
pip install -e .

flask run -h ${HOST} -p ${PORT} --with-threads --reload --debugger
