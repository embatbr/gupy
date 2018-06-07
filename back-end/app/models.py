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
        return ',\n'.join(["%s: '%s'" % (k, v) for (k, v) in self.fields.items()])

    def __str__(self):
        return self.__repr__()

    @property
    def insert_query(self):
        field_names = self._get_fields()
        field_refs = ['%({})s'.format(field_name) for field_name in field_names]

        sql = "INSERT INTO {schema}.{table} ({fields}) VALUES ({values}) RETURNING id"
        return sql.format(**{
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
            'city': city if city else None,
            'neighborhood': neighborhood if neighborhood else None,
            'place_name': place_name if place_name else None,
            'place_number': place_number if place_number else None,
            'place_complement': place_complement if place_complement else None,
            'cep': cep if cep else None,
            'latitude': latitude if latitude else None,
            'longitude': longitude if longitude else None
        })

    def save(self, db_cur):
        values = dict(self.fields)

        try:
            db_cur.execute(self.insert_query, values)
            _id = db_cur.fetchone()[0]
            return _id

        except psycopg2.IntegrityError as error:
            util.handle_not_null_violation(error, self._resource)
            raise error

        except Exception as error:
            util.handle_enum_violation('recruitment.brazilian_states', 'state',
                error, self._resource)
            util.handle_character_field_overflow(error, self._resource)
            util.handle_numeric_field_overflow(error, self._resource)
            raise error


class CandidateModel(Model):

    def __init__(self, name, image_name, birthdate, gender, email, phone, tags):
        super(CandidateModel, self).__init__('candidate', 'recruitment', 'candidates', {
            'name': name if name else None,
            'image_path': '%s_%s' % (str2base64(email), image_name),
            'birthdate': birthdate if birthdate else None,
            'gender': gender.upper() if gender else None,
            'email': email.lower() if email else None,
            'phone': phone if phone else None,
            'tags': tags if tags else None,
            'address_id': None
        })

    def save(self, db_cur, address_id):
        self.fields['address_id'] = address_id
        values = dict(self.fields)

        try:
            values['tags'] = json.dumps(values['tags'])
            db_cur.execute(self.insert_query, values)
            _id = db_cur.fetchone()[0]
            return _id

        except psycopg2.IntegrityError as error:
            util.handle_unique_violation(error, self._resource, 'email', self.fields['email'])
            util.handle_not_null_violation(error, self._resource)
            raise error

        except Exception as error:
            util.handle_enum_violation('recruitment.genders', 'gender',
                error, self._resource)
            util.handle_date_or_time_out_of_range(error, self._resource, 'birthdate')
            util.handle_character_field_overflow(error, self._resource)
            raise error


class ExperienceModel(Model):

    def __init__(self, _type, institution_name, title, start_date, end_date, description):
        super(ExperienceModel, self).__init__('experience', 'recruitment', 'experiences', {
            '_type': _type.upper() if _type else None,
            'institution_name': institution_name if institution_name else None,
            'title': title if title else None,
            'start_date': start_date if start_date else None,
            'end_date': end_date if end_date else None,
            'description': description if description else None,
            'candidate_id': None
        })

    def save(self, db_cur, candidate_id):
        self.fields['candidate_id'] = candidate_id
        values = dict(self.fields)

        try:
            db_cur.execute(self.insert_query, values)

        except psycopg2.IntegrityError as error:
            util.handle_not_null_violation(error, self._resource)
            raise error

        except Exception as error:
            util.handle_date_or_time_out_of_range(error, self._resource, None)
            raise error
