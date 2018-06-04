"""A controller manages the HTTP flow for a given resource.
"""


import falcon
import json

import app.util as util


embody = lambda req: json.loads(str(req.stream.read(req.content_length), 'utf-8'))

has_payload = lambda body: isinstance(body, dict) and body


class Controller(object):

    def __init__(self, domains):
        self.domains = domains


class CandidateController(Controller):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'message': 'Should retrieve information about a candidate'
        })

    def on_post(self, req, resp):
        body = None

        try:
            body = embody(req)
            if not has_payload(body):
                raise Exception('Payload must be a non-empty JSON object')
        except Exception as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                'err': str(err)
            })
            return

        try:
            self.domains['create'].apply([body])

        except Exception as err:
            is_domain_err = isinstance(err, util.DomainError)

            resp.status = falcon.HTTP_403 if is_domain_err else falcon.HTTP_400
            resp.body = json.dumps({
                'err': err.show() if is_domain_err else str(err)
            })
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'message': 'Candidate profile successfully created'
        })
