#!/bin/sh
export FLASK_APP=./index.py

# for development only:
uv run flask --app index run --debug -h 0.0.0.0

# in production: 
# uv run flask --app index run