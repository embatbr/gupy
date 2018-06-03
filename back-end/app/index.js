'use strict';


const restify = require("restify");

const settings = require('./settings')
const endpoints = require('./endpoints');
let logic = require('./logic');
const storages = require('./storages');


function Application(settings, endpoints) {
    this.port = settings.port;
    this.endpoints = endpoints

    this.server = restify.createServer();

    this.run = (candidate_logic) => {
        this.server.use(restify.plugins.bodyParser({
            mapParams: true
        }));

        for(const endpoint in this.endpoints) {
            const objs = this.endpoints[endpoint];
            objs.forEach((obj) => {
                const verb = obj['verb'];
                const method = obj['method'];
                const action = obj['action'];

                this.server[method](`/${endpoint}`, candidate_logic[action]);
            });
        }

        this.server.listen(this.port, () => {
            console.log('Listening to port', this.port)
        });
    };
};


let file_handler = new storages.FileHandler();
let database = new storages.Database(settings.database);
let candidate_logic = new logic.CandidateLogic(file_handler, database);

var app = new Application(settings.app, endpoints);
app.run(candidate_logic);
