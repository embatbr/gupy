"""Common code.
"""


import base64
import json
import os
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


def dimension_name():
    letter = chr(random.randint(65, 90))
    number = random.randint(1, 100000)
    return '%s%d' % (letter, number)

def photo_name():
    return 'rick-%d.png' % random.randint(1, 9)

def email_address(name):
    username = '.'.join(name.split(' ')[::-1]).lower()
    return '%s@citadel_of_ricks.com' % username

def choose_gender():
    number = random.randint(0, 100)

    if number < 50:
        return 'MALE'
    if number <= 100:
        return 'FEMALE'


def gen_json_data(name, photo, email, gender):
    return {
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Jardins',
            'place_name': 'R. Pamplona',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        },
        'professional_experiences': [
            {
                'institution_name': 'Laboratório do Multiverso',
                'title': 'Cientista Maluco',
                'start_date': '1990-06-01',
                'end_date': None,
                'description': 'Lot of stuff'
            },
            {
                'institution_name': 'My Garage',
                'title': 'Cientista "normal"',
                'start_date': '1970-01-01',
                'end_date': '1990-05-31',
                'description': 'Normal nerdy stuff'
            }
        ],
        'educational_experiences': [
            {
                'institution_name': 'Escola da Vida',
                'title': 'Vagabundo',
                'start_date': '1960-01-01',
                'end_date': None,
                'description': 'Escola é chato'
            }
        ]
    }
