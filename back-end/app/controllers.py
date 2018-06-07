"""A controller manages the HTTP flow for a given resource.
"""


import falcon
import json

import app.util as util


def _extract_payload(payload_type, req, resp):
    try:
        stream = req.stream.read(req.content_length)
        payload = json.loads(str(stream, 'utf-8'))
        assert isinstance(payload, payload_type) and payload
        return payload
    except Exception as error:
        raise Exception('Payload must be a non-empty JSON object')


class Controller(object):

    def __init__(self, actions):
        self.actions = actions

    # TODO create a "_exec_request" method to encapsulate all "on_" methods

    def on_post(self, req, resp, is_batch):
        try:
            payload = _extract_payload(list if is_batch else dict, req, resp)

            self.actions['create'].execute(payload if is_batch else [payload])

            plural = 's' if is_batch else ''
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                'message': 'Candidate{0} profile{0} successfully created'.format(plural)
            })

        except Exception as err:
            is_action_err = isinstance(err, util.ActionError)

            resp.status = falcon.HTTP_403 if is_action_err else falcon.HTTP_400
            resp.body = json.dumps({
                'err': err.show() if is_action_err else str(err)
            })


class ProfileController(Controller):

    def on_post(self, req, resp):
        super(ProfileController, self).on_post(req, resp, False)

    def on_get(self, req, resp):
        try:
            params = req.params

            profile = self.actions['read'].execute(params)

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(profile)

        except Exception as err:
            is_action_err = isinstance(err, util.ActionError)

            resp.status = falcon.HTTP_403 if is_action_err else falcon.HTTP_400
            resp.body = json.dumps({
                'err': err.show() if is_action_err else str(err)
            })


class ProfileBatchController(Controller):

    def on_post(self, req, resp):
        super(ProfileBatchController, self).on_post(req, resp, True)
