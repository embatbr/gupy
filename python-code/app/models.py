"""Deals with persistence
"""


import base64
import json
import psycopg2

import app.util as util


str2base64 = lambda s: base64.b64encode(bytes(s.encode('utf-8'))).decode('utf-8')


class Model(object):

    def __init__(self, _resource, _pg_schema_name, _pg_table_name, fields=dict):
        self._resource = _resource

        self._pg_schema_name = _pg_schema_name
        self._pg_table_name = _pg_table_name

        self.fields = fields

    def _get_fields(self):
        return list(self.fields.keys())

    def __repr__(self):
        fields = self._get_fields()
        return ',\n'.join(["%s: '%s'" % (field, getattr(self, field)) for field in fields])

    def __str__(self):
        return self.__repr__()

    @property
    def insert_query(self):
        field_names = self._get_fields()
        field_refs = ['%({})s'.format(field_name) for field_name in field_names]

        return "INSERT INTO {schema}.{table} ({fields}) VALUES ({values})".format(**{
            'schema': self._pg_schema_name,
            'table': self._pg_table_name,
            'fields': ", ".join(field_names),
            'values': ", ".join(field_refs)
        })


class AddressModel(Model):

    def __init__(self, state, city, neighborhood, place_name, place_number,
                 place_complement, cep, latitude, longitude):
        super(AddressModel, self).__init__('address', 'recruitment', 'addresses', {
            'state': state.upper() if state else None,
            'city': city,
            'neighborhood': neighborhood,
            'place_name': place_name,
            'place_number': place_number,
            'place_complement': place_complement,
            'latitude': latitude,
            'longitude': longitude,
            'cep': cep,
        })

    def save(self, db_cur):
        query = "{} RETURNING id".format(self.insert_query)
        values = dict(self.fields)

        try:
            db_cur.execute(query, values)
            return db_cur.fetchone()[0]

        except psycopg2.IntegrityError as err:
            msg = 'null value in column'
            if str(err).startswith(msg):
                raise util.DatabaseConstraintViolationError(
                    self._resource, None, None,
                    util.DatabaseConstraintViolationError.NOT_NULL
                )

        except Exception as err:
            msg = 'invalid input value for enum recruitment.brazilian_states'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, 'state')

            msg = 'value too long for type character'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, None)

            msg = 'numeric field overflow'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, None)

            print()
            print(err)
            print()


class CandidateModel(Model):

    def __init__(self, name, image_name, birthdate, gender, email, phone, tags):
        super(CandidateModel, self).__init__('candidate', 'recruitment', 'candidates', {
            'name': name,
            'image_path': '%s_%s' % (str2base64(email), image_name),
            'birthdate': birthdate,
            'gender': gender.upper() if gender else None,
            'email': email.lower() if email else None,
            'phone': phone,
            'tags': tags,
            'address_id': None
        })

    def save(self, db_cur, address_id):
        self.fields['address_id'] = address_id

        query = self.insert_query
        values = dict(self.fields)

        try:
            values['tags'] = json.dumps(values['tags'])

            db_cur.execute(query, values)

        except psycopg2.IntegrityError as err:
            msg = 'duplicate key value violates unique constraint "candidates_email_key"'
            if str(err).startswith(msg):
                raise util.DatabaseConstraintViolationError(
                    self._resource, 'email', self.fields['email'],
                    util.DatabaseConstraintViolationError.UNIQUE
                )

            msg = 'null value in column'
            if str(err).startswith(msg):
                raise util.DatabaseConstraintViolationError(
                    self._resource, None, None,
                    util.DatabaseConstraintViolationError.NOT_NULL
                )

        except Exception as err:
            msg = 'invalid input value for enum recruitment.candidate_genders'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, 'gender')

            msg = 'date/time field value out of range'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, 'birthdate')

            msg = 'value too long for type character'
            if str(err).startswith(msg):
                raise util.DatabaseInvalidValueError(self._resource, None)
