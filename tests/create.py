"""Tests for the Create part of CRUD.
"""


import os
import psycopg2
import requests as r


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


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    data={
        'name': 'John Doe',
        'image': 'put some image here',
        'birthdate': '1970-01-01',
        'gender': 'Male',
        'email': 'john.doe@email.com',
        'phone': '11987654321',
        'tags': ['python', 'java']
    }
)

print(resp)
