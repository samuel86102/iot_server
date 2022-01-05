#!/bin/sh
gunicorn -w 4 -b 0.0.0.0:8787 main:app
