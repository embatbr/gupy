"""Deals with persistence
"""


class Model(object):
    pass


class CandidateModel(Model):
    PG_SCHEMA_NAME = 'recruitment'
    PG_TABLE_NAME = 'candidates'

    def __init__(self, name, image_name, birthdate, gender, email, phone):
        self.name = name
        self.image_name = image_name
        self.birthdate = birthdate
        self.gender = gender.upper()
        self.email = email.lower()
        self.phone = phone

        self.__validate()

    def get_fields(self):
        return list(self.__dict__.keys())

    def __validate(self):
        pass

    def __repr__(self):
        fields = self.get_fields()
        return ',\n'.join(["%s: '%s'" % (field, getattr(self, field)) for field in fields])

    def __str__(self):
        return self.__repr__()

    def get_insert_query(self):
        fields = self.get_fields()
        values = ['%({})s'.format(field) for field in fields]

        return "INSERT INTO {schema}.{table}({fields}) VALUES ({values})".format(**{
            'schema': CandidateModel.PG_SCHEMA_NAME,
            'table': CandidateModel.PG_TABLE_NAME,
            'fields': ", ".join(fields),
            'values': ", ".join(values)
        })

    def save(self, db_cur):
        query = self.get_insert_query()
        db_cur.execute(query, self.__dict__)
