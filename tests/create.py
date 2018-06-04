"""Tests for the Create part of CRUD.
"""


from common import *


def test(name, expected, given):
    try:
        print("'{}'".format(name))
        print('expected:', expected)
        print('given:', given)
        print('result:', end=' ')
        assert given == expected
        print('SUCCESS')
    except AssertionError as err:
        print('FAILURE')
    finally:
        print(resp.text)
        print()


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    }
)

test('POST should return 400 when body is not present', 400, resp.status_code)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data='not a JSON'
)

test('POST should return 400 when body is not a JSON', 400, resp.status_code)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data={}
)

test('POST should return 400 when body is an empty JSON', 400, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
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
    })
)

test('POST should return 200 when body is a non-empty valid JSON', 200, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': 'RJ',
            'city': 'Rio de Janeiro',
            'neighborhood': 'Copacabana',
            'place_name': 'R. do Favelão',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when email is repeated', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': 'SHEMALE',
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when gender is not allowed', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': 'ZZ',
            'city': 'Cidade Z',
            'neighborhood': 'Cidade Fantasma',
            'place_name': 'R. de Saitama',
            'place_number': 's/n',
            'place_complement': 'apartmento 4',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when state is not allowed', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-13-01',
        'gender': gender,
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when birthdate is incorrect', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': None,
        'tags': ['python', 'java'],
        'address': {
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when phone null', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': '11987654321',
        'tags': ['python', 'java'],
        'address': {
            'state': None,
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when state null', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
        'name': name,
        'image_name': photo,
        'birthdate': '1948-01-01',
        'gender': gender,
        'email': email,
        'phone': '119876543210',
        'tags': ['python', 'java'],
        'address': {
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 phone value overflows', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
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
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-1001',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 cep value overflows', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
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
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -123.5647577,
            'longitude': -46.6518495
        }
    })
)

test('POST should return 403 when coordinate precision overflows', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
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
                'institution_name': None,
                'title': 'Vagabundo',
                'start_date': '1960-01-01',
                'end_date': None,
                'description': 'Escola é chato'
            }
        ]
    })
)

test('POST should return 403 when institution_name is null', 403, resp.status_code)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps({
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
                'start_date': '1960-13-01',
                'end_date': None,
                'description': 'Escola é chato'
            }
        ]
    })
)

test('POST should return 403 when date is incorrect', 403, resp.status_code)
