#!/bin/bash

# Create logs directory
mkdir -p logs

# Start Gunicorn
gunicorn --config gunicorn.conf.py wsgi:app