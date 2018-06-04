"""Tests for the Create (in batch) part of CRUD.
"""


from common import *


resp = r.post(
    'http://{host}:{port}/profiles'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    }
)

test('POST should return 400 when body is not present', 400, resp)


resp = r.post(
    'http://{host}:{port}/profiles'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data='not a JSON'
)

test('POST should return 400 when body is not a JSON', 400, resp)


resp = r.post(
    'http://{host}:{port}/profiles'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data={}
)

test('POST should return 400 when body is an empty JSON', 400, resp)


names = [
    'Rick Sanchez %s' % dimension_name(),
    'Rick Sanchez %s' % dimension_name(),
    'Rick Sanchez %s' % dimension_name()
]

resp = r.post(
    'http://{host}:{port}/profiles'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data=json.dumps([
        gen_json_data(names[0], photo_name(), email_address(names[0]), choose_gender()),
        gen_json_data(names[1], photo_name(), email_address(names[1]), choose_gender()),
        gen_json_data(names[2], photo_name(), email_address(names[2]), choose_gender())
    ])
)

test('POST should return 200 when body is a non-empty valid JSON', 200, resp)
