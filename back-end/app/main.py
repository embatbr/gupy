"""Flash point for the application.
"""


import falcon

import app.controllers as controllers
import app.domains as domains
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
        'create': domains.DomainCreate(settings.DB_CONNECTION, model_inits),
        'read': domains.DomainRead(settings.DB_CONNECTION, model_inits)
    }),
    'profiles': controllers.ProfileBatchController({
        'create': domains.DomainCreate(settings.DB_CONNECTION, model_inits)
    })
}

restful_application = RESTfulApplication(application, routes)
restful_application.expose()
