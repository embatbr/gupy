"""Deals with persistence
"""


class Model(object):
    def __init__(self, _pg_schema_name, _pg_table_name, fields=dict):
        self._pg_schema_name = _pg_schema_name
        self._pg_table_name = _pg_table_name

        self.fields = fields

    def _get_fields(self):
        return list(self.fields.keys())

    def get_insert_query(self):
        field_names = self._get_fields()
        field_refs = ['%({})s'.format(field_name) for field_name in field_names]

        return "INSERT INTO {schema}.{table}({fields}) VALUES ({values})".format(**{
            'schema': self._pg_schema_name,
            'table': self._pg_table_name,
            'fields': ", ".join(field_names),
            'values': ", ".join(field_refs)
        })


class CandidateModel(Model):

    def __init__(self, name, image_name, birthdate, gender, email, phone):
        super(CandidateModel, self).__init__('recruitment', 'candidates', {
            'name': name,
            'image_name': image_name,
            'birthdate': birthdate,
            'gender': gender.upper(),
            'email': email.lower(),
            'phone': phone
        })

        self._validate()

    def _validate(self):
        pass

    def __repr__(self):
        fields = self._get_fields()
        return ',\n'.join(["%s: '%s'" % (field, getattr(self, field)) for field in fields])

    def __str__(self):
        return self.__repr__()

    def save(self, db_cur):
        query = self.get_insert_query()
        db_cur.execute(query, self.fields)
