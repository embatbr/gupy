"use strict";


let restify = require("restify");


function RESTfulServer(routes) {
    this.port = process.env.PORT || 8000;
    this.routes = routes

    this.server = restify.createServer();

    this.expose = (controllers) => {
        for(let endpoint in this.routes) {
            let verbs = this.routes[endpoint];

            for(let verb in verbs) {
                let method = verbs[verb]['method'];
                let action = verbs[verb]['action'];

                console.log('exposing', endpoint, verb, method, action);

                let controller = new controllers[`${endpoint}`]();
                this.server[method](`/${endpoint}`, controller[action]);
            }
        }

        this.server.listen(this.port, () => {
            console.log('Listening to port', this.port)
        });
    };
};


module.exports = {
    RESTfulServer: RESTfulServer
};
