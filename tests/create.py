"""Tests for the Create part of CRUD.
"""


from common import *


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    }
)

test('POST should return 400 when body is not present', 400, resp)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data='not a JSON'
)

test('POST should return 400 when body is not a JSON', 400, resp)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data={}
)

test('POST should return 400 when body is an empty JSON', 400, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 200 when body is a non-empty valid JSON', 200, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when email is repeated', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
data=gen_json_data(name, photo, email, 'SHEMALE')

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when gender is not allowed', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['address'] = {
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

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when state is not allowed', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['birthdate'] = '1948-13-01'

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when birthdate is incorrect', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['phone'] = None

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when phone null', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['address']['state'] = None

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when state null', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['phone'] = '119876543210'

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 phone value overflows', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['address']['cep'] = '01310-1001'

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 cep value overflows', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['address']['latitude'] = -123.5647577

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when coordinate precision overflows', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['educational_experiences'][0]['institution_name'] = None

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when institution_name is null', 403, resp)


name = 'Rick Sanchez %s' % dimension_name()
photo = photo_name()
email = email_address(name)
gender = choose_gender()
data=gen_json_data(name, photo, email, gender)
data['educational_experiences'][0]['start_date'] = '1960-13-01'

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps(data)
)

test('POST should return 403 when date (in experience) is incorrect', 403, resp)
