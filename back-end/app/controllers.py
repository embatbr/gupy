"""A controller manages the HTTP flow for a given resource.
"""


import falcon
import json

import app.util as util


def _extract_body(body_type, req, resp):
    stream = req.stream.read(req.content_length)
    body = json.loads(str(stream, 'utf-8'))
    assert isinstance(body, body_type) and body, 'Payload must be a non-empty JSON object'
    return body


class Controller(object):

    def __init__(self, domains):
        self.domains = domains

    def on_post(self, req, resp, is_batch):
        try:
            body = _extract_body(list if is_batch else dict, req, resp)

            self.domains['create'].apply(body if is_batch else [body])

            resp.status = falcon.HTTP_200
            plural = 's' if is_batch else ''
            resp.body = json.dumps({
                'message': 'Candidate{0} profile{0} successfully created'.format(plural)
            })

        except Exception as err:
            is_domain_err = isinstance(err, util.DomainError)

            resp.status = falcon.HTTP_403 if is_domain_err else falcon.HTTP_400
            resp.body = json.dumps({
                'err': err.show() if is_domain_err else str(err)
            })


class ProfileController(Controller):

    def on_post(self, req, resp):
        super(ProfileController, self).on_post(req, resp, False)

    def on_get(self, req, resp):
        params = req.params

        try:
            profile = self.domains['read'].apply(params)

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(profile)

        except Exception as err:
            is_domain_err = isinstance(err, util.DomainError)

            resp.status = falcon.HTTP_403 if is_domain_err else falcon.HTTP_400
            resp.body = json.dumps({
                'err': err.show() if is_domain_err else str(err)
            })


class ProfileBatchController(Controller):

    def on_post(self, req, resp):
        super(ProfileBatchController, self).on_post(req, resp, True)
