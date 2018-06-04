"""Problems' domains (aka business logic).
"""


import psycopg2

import app.util as util


class Domain(object):

    def __init__(self, db_conn_params, models):
        self.db_conn_params = db_conn_params
        self.models = models


class DomainCreate(Domain):

    def apply(self, artifacts):
        batch_models = list()

        for artifact in artifacts:
            batch_models.append({
                'address': self.models['address'](*[
                    artifact['address']['state'],
                    artifact['address']['city'],
                    artifact['address']['neighborhood'],
                    artifact['address']['place_name'],
                    artifact['address']['place_number'],
                    artifact['address']['place_complement'],
                    artifact['address']['cep'],
                    artifact['address']['latitude'],
                    artifact['address']['longitude']
                ]),
                'candidate': self.models['candidate'](*[
                    artifact['name'],
                    artifact['image_name'],
                    artifact['birthdate'],
                    artifact['gender'],
                    artifact['email'],
                    artifact['phone'],
                    artifact['tags']
                ])
            })

        try:
            db_conn = psycopg2.connect(**self.db_conn_params)
            db_cur = db_conn.cursor()

            for model in batch_models:
                address_id = model['address'].save(db_cur)
                model['candidate'].save(db_cur, address_id)

            db_conn.commit()

        except util.DatabaseConstraintViolationError as err:
            if err.constraint == util.DatabaseConstraintViolationError.UNIQUE:
                reason = "%s '%s' already exists" % (err.field_name, err.field_value)
                raise util.DomainError('create', err.resource, reason)

            if err.constraint == util.DatabaseConstraintViolationError.NOT_NULL:
                reason = "Null value for non-nullable field"
                raise util.DomainError('create', err.resource, reason)

        except util.DatabaseInvalidValueError as err:
            reason = "Value invalid or too long for field"
            if err.field_name:
                reason = "%s '%s'" % (reason, err.field_name)
            raise util.DomainError('create', err.resource, reason)

        finally:
            db_conn.close()
