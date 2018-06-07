"""
"""


import os


# In a production environment, writer could act on a master and reader on a replica
DB_CONNECTION = {
    'writer': {
        'host': os.environ.get('DB_HOST_WRITER', 'localhost'),
        'port': int(os.environ.get('DB_PORT_WRITER', '5432')),
        'dbname': os.environ.get('DB_NAME_WRITER', 'gupy'),
        'user': os.environ.get('DB_USER_WRITER', 'gupy_writer'),
        'password': os.environ.get('DB_PASSWORD_WRITER', 'gupy_writer')
    },
    'reader': {
        'host': os.environ.get('DB_HOST_READER', 'localhost'),
        'port': int(os.environ.get('DB_PORT_READER', '5432')),
        'dbname': os.environ.get('DB_NAME_READER', 'gupy'),
        'user': os.environ.get('DB_USER_READER', 'gupy_reader'),
        'password': os.environ.get('DB_PASSWORD_READER', 'gupy_reader')
    }
}
