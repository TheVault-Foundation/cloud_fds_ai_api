#!/bin/sh
cd src
gunicorn -w 4 -b 0.0.0.0:6000 "api:app"
