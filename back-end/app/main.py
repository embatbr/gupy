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

routes = {
    'candidate': controllers.CandidateController({
        'create': domains.DomainCreate(settings.DB_CONNECTION, {
            'candidate': models.CandidateModel,
            'address': models.AddressModel,
            'experience': models.ExperienceModel
        })
    }),
    'candidates': controllers.CandidateBatchController({
        'create': domains.DomainCreate(settings.DB_CONNECTION, {
            'candidate': models.CandidateModel,
            'address': models.AddressModel,
            'experience': models.ExperienceModel
        })
    })
}

restful_application = RESTfulApplication(application, routes)
restful_application.expose()
