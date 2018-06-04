"""Problems' domains (aka business logic).
"""


import psycopg2

import app.util as util


class Domain(object):

    def __init__(self, db_conn_params, models):
        self.db_conn_params = db_conn_params
        self.models = models


class CreateDomain(Domain):

    def apply(self, artifacts):
        batch_models = list()

        for artifact in artifacts:
            batch_models.append({
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

        resources = ['candidate']
        resource_log = None

        try:
            db_conn = psycopg2.connect(**self.db_conn_params)
            db_cur = db_conn.cursor()

            for model in batch_models:
                for resource in resources:
                    resource_log = resource
                    model[resource].save(db_cur)

            db_conn.commit()

        except util.DatabaseConstraintViolationError as err:
            if err.constraint == util.DatabaseConstraintViolationError.UNIQUE:
                reason = "%s '%s' already exists" % (err.field_name, err.field_value)
                raise util.DomainError('create', resource_log, reason)

        except util.DatabaseInvalidValueError as err:
            reason = "Invalid value for field '%s'" % err.field_name
            raise util.DomainError('create', resource_log, reason)

        finally:
            db_conn.close()
