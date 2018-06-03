"""Problems' domains (aka business logic).
"""


import psycopg2


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
                    artifact['phone']
                ])
            })

        db_conn = psycopg2.connect(**self.db_conn_params)
        db_cur = db_conn.cursor()

        for model in batch_models:
            print(model['candidate'].get_insert_query())
            model['candidate'].save(db_cur)

        db_conn.commit()
        db_conn.close()
