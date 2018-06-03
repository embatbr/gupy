"""Common code.
"""


import base64
import json
import os
import psycopg2
import random
import requests as r
import uuid


app_conn_settings = {
    'host': os.environ.get('SERVER_HOST', 'localhost'),
    'port': os.environ.get('SERVER_PORT', 8000)
}

db_conn_settings = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 5432),
    'dbname': os.environ.get('DB_NAME', 'gupy'),
    'user': os.environ.get('DB_USER', 'gupy'),
    'password': os.environ.get('DB_PASSWORD', 'gupy')
}