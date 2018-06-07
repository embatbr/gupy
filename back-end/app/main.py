"""Flash point for the application.
"""


import falcon

import app.controllers as controllers
import app.actions as actions
import app.models as models
import app.settings as settings


class RESTfulApplication(object):

    def __init__(self, application, routes):
        self.application = application
        self.routes = routes

    def expose(self):
        for (endpoint, controller) in self.routes.items():
            self.application.add_route('/{}'.format(endpoint), controller)


application = falcon.API()

model_inits = {
    'candidate': models.CandidateModel,
    'address': models.AddressModel,
    'experience': models.ExperienceModel
}

routes = {
    'profile': controllers.ProfileController({
        'create': actions.CreateAction(settings.DB_CONNECTION['writer'], model_inits),
        'read': actions.ReadAction(settings.DB_CONNECTION['reader'], model_inits)
    }),
    'profiles': controllers.ProfileBatchController({
        'create': actions.CreateAction(settings.DB_CONNECTION['writer'], model_inits)
    })
}

restful_application = RESTfulApplication(application, routes)
restful_application.expose()
