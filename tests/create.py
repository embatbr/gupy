"""Tests for the Create part of CRUD.
"""


from common import *


name = uuid.uuid4().hex
(first_name, last_name) = (name[ : random.randint(3, 5)],
                           name[random.randint(5, 10) : random.randint(15, 20)])

resp = r.post(
    'http://{host}:{port}/candidate'.format(**app_conn_settings),
    data={
        'name': '%s %s' % (first_name, last_name),
        'image_name': 'mickey.jpg',
        'image_data': base64.b64encode(open('./mickey.jpg', 'rb').read()),
        'birthdate': '1990-01-01',
        'gender': 'Male',
        'email': '%s.%s@email.com' % (first_name.lower(), last_name.lower()),
        'phone': '11987654321',
        'address': json.dumps({
            'state': 'SP',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'place_name': 'Av. Paulista',
            'place_number': '1000',
            'place_complement': 'apartmento 10',
            'cep': '01310-100',
            'latitude': -23.5647577,
            'longitude': -46.6518495
        }),
        'tags': json.dumps(['python', 'java']),
        'professional_experiences': json.dumps([
            {
                'institution_name': 'Gupy',
                'title': 'Developer',
                'start_date': '2017-09-15',
                'description': 'developer stuff too, but with more money'
            },
            {
                'institution_name': 'Revelo',
                'title': 'Developer',
                'start_date': '2015-01-20',
                'end_date': '2017-08-10',
                'description': 'developer stuff'
            },
            {
                'institution_name': 'Freelancer',
                'title': 'Developer',
                'start_date': '2010-01-01'
            }
        ]),
        'educational_experiences': json.dumps([
            {
                'institution_name': 'Random MBA College',
                'title': 'MBA',
                'start_date': '2018-02-01',
                'end_date': None
            },
            {
                'institution_name': 'not MIT',
                'title': 'Computer Science',
                'start_date': '2010-02-01',
                'end_date': '2015-05-20'
            }
        ])
    }
)

print(resp)
print(resp.json())
