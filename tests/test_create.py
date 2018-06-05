"""Tests for the Create part of CRUD.
"""


import unittest

from util import *


BASE_URL = 'http://{host}:{port}'.format(**app_conn_settings)


class TestCreate(unittest.TestCase):

    URL = '%s/profile' % BASE_URL

    def setUp(self):
        self.name = 'Rick Sanchez %s' % dimension_name()
        self.photo = photo_name()
        self.email = email_address(self.name)
        self.gender = choose_gender()
        self.data=gen_json_data(self.name, self.photo, self.email, self.gender)

    def test_post_without_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_no_json_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data='not a JSON'
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_empty_json_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data={}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_valid_json_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'message': 'Candidate profile successfully created'
        })

    def test_post_with_repeated_email(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'message': 'Candidate profile successfully created'
        })

        name = 'Rick Sanchez %s' % dimension_name()
        photo = photo_name()
        gender = choose_gender()
        data=gen_json_data(name, photo, self.email, gender)

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': "email '%s' already exists" % self.email,
                'resource': 'candidate',
                'action': 'create'
            }
        })

    def test_post_with_not_permitted_gender(self):
        self.data['gender'] = 'SHEMALE'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': "Value invalid or too long for field 'gender'",
                'resource': 'candidate',
                'action': 'create'
            }
        })

    def test_post_with_not_permitted_state(self):
        self.data['address']['state'] = 'ZZ'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': "Value invalid or too long for field 'state'",
                'resource': 'address',
                'action': 'create'
            }
        })

    def test_post_with_incorrect_birthdate(self):
        self.data['birthdate'] = '1948-13-01'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': "Value invalid or too long for field 'birthdate'",
                'resource': 'candidate',
                'action': 'create'
            }
        })

    def test_post_with_phone_null(self):
        self.data['phone'] = None

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Null value for non-nullable field',
                'resource': 'candidate',
                'action': 'create'
            }
        })

    def test_post_with_state_null(self):
        self.data['address']['state'] = None

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Null value for non-nullable field',
                'resource': 'address',
                'action': 'create'
            }
        })

    def test_post_with_overflown_phone(self):
        self.data['phone'] = '119876543210'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Value invalid or too long for field',
                'resource': 'candidate',
                'action': 'create'
            }
        })

    def test_post_with_overflown_cep(self):
        self.data['address']['cep'] = '12345-6789'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Value invalid or too long for field',
                'resource': 'address',
                'action': 'create'
            }
        })

    def test_post_with_overflown_coordinate(self):
        self.data['address']['latitude'] = -123.5647577

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Value invalid or too long for field',
                'resource': 'address',
                'action': 'create'
            }
        })

    def test_post_with_null_institution(self):
        self.data['educational_experiences'][0]['institution_name'] = None

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Null value for non-nullable field',
                'resource': 'experience',
                'action': 'create'
            }
        })

    def test_post_with_incorrect_experience_date(self):
        self.data['educational_experiences'][0]['start_date'] = '1960-13-01'

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(self.data)
        )

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            'err': {
                'reason': 'Value invalid or too long for field',
                'resource': 'experience',
                'action': 'create'
            }
        })


class TestBatchCreate(unittest.TestCase):

    URL = '%s/profiles' % BASE_URL

    def test_post_without_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_no_json_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data='not a JSON'
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_empty_json_payload(self):
        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data={}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            'err': 'Payload must be a non-empty JSON object'
        })

    def test_post_with_valid_json_payload(self):
        names = [
            'Rick Sanchez %s' % dimension_name(),
            'Rick Sanchez %s' % dimension_name(),
            'Rick Sanchez %s' % dimension_name()
        ]

        resp = r.post(
            TestCreate.URL,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps([
                gen_json_data(names[0], photo_name(), email_address(names[0]), choose_gender()),
                gen_json_data(names[1], photo_name(), email_address(names[1]), choose_gender()),
                gen_json_data(names[2], photo_name(), email_address(names[2]), choose_gender())
            ])
        )


if __name__ == '__main__':
    unittest.main()
