#!/bin/sh
gunicorn -w 4 -b 0.0.0.0:6000 "api:src"