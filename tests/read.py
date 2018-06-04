"""Tests for the Read part of CRUD.
"""


from common import *


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

if resp.status_code == 200:
    resp = r.get(
        'http://{host}:{port}/candidate'.format(**app_conn_settings),
        params={
            'email': email
        }
    )

    print(resp)
    print(resp.text)
