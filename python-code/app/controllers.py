"""A controller manages the HTTP flow for a given resource.
"""


import falcon
import json


embody = lambda req: json.loads(str(req.stream.read(req.content_length), 'utf-8'))

has_payload = lambda body: isinstance(body, dict) and body


class Controller(object):

    def __init__(self, domains):
        self.domains = domains


class CandidateController(Controller):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'msg': 'Should retrieve information about a candidate'
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
                'msg': str(err)
            })
            return

        self.domains['create'].apply([body])

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'msg': 'Should insert information of a candidate'
        })
