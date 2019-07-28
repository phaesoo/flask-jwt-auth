#!/bin/bash

HOST=ec2-3-87-70-34.compute-1.amazonaws.com
PORT=5000

export FLASK_APP=flask-jwt-auth-example
export FLASK_ENV=debug
export FLASK_DEBUG=1
rm -rf src.egg-info
pip install -e .

flask run -h ${HOST} -p ${PORT} --with-threads --reload --debugger