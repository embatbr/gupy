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
        print(resp.text)
    except AssertionError as err:
        print('FAILURE')
    finally:
        print()


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    }
)

test('POST should return 400 when body is not present', resp.status_code, 400)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data='not a JSON'
)

test('POST should return 400 when body is not a JSON', resp.status_code, 400)


resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    headers={
        'content-type': 'application/json'
    },
    data={}
)

test('POST should return 400 when body is an empty JSON', resp.status_code, 400)


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
        'gender': 'Male',
        'email': email,
        'phone': '11987654321'
    })
)

test('POST should return 200 when body is a non-empty valid JSON', resp.status_code, 200)


# resp = r.post(
#     'http://{host}:{port}/candidate'.format(**app_conn_settings),
#     headers={
#         'content-type': 'application/json'
#     },
#     data={
#         'name': '%s %s' % (first_name, last_name),
#         'image_name': 'rick.png',
#         'image_data': base64.b64encode(open('./rick.png', 'rb').read()),
#         'birthdate': '1948-01-01',
#         'gender': 'Male',
#         'email': '%s.%s@email.com' % (first_name.lower(), last_name.lower()),
#         'phone': '11987654321',
#         'address': {
#             'state': 'SP',
#             'city': 'São Paulo',
#             'neighborhood': 'Bela Vista',
#             'place_name': 'Av. Paulista',
#             'place_number': '1000',
#             'place_complement': 'apartmento 10',
#             'cep': '01310-100',
#             'latitude': -23.5647577,
#             'longitude': -46.6518495
#         },
#         'tags': ['python', 'java'],
#         'professional_experiences': [
#             {
#                 'institution_name': 'Gupy',
#                 'title': 'Developer',
#                 'start_date': '2017-09-15',
#                 'description': 'developer stuff too, but with more money'
#             },
#             {
#                 'institution_name': 'Revelo',
#                 'title': 'Developer',
#                 'start_date': '2015-01-20',
#                 'end_date': '2017-08-10',
#                 'description': 'developer stuff'
#             },
#             {
#                 'institution_name': 'Freelancer',
#                 'title': 'Developer',
#                 'start_date': '2010-01-01'
#             }
#         ],
#         'educational_experiences': [
#             {
#                 'institution_name': 'Random MBA College',
#                 'title': 'MBA',
#                 'start_date': '2018-02-01',
#                 'end_date': None
#             },
#             {
#                 'institution_name': 'not MIT',
#                 'title': 'Computer Science',
#                 'start_date': '2010-02-01',
#                 'end_date': '2015-05-20'
#             }
#         ]
#     }
# )
