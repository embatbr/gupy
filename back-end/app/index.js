'use strict';


const restify = require("restify");

const settings = require('./settings')
const endpoints = require('./endpoints');
let logics = require('./logics');
const storages = require('./storages');


function Application(settings, endpoints) {
    this.port = settings.port;
    this.endpoints = endpoints

    this.server = restify.createServer();

    this.run = (logics, file_handler, database) => {
        this.server.use(restify.plugins.bodyParser({
            mapParams: true
        }));

        for(const endpoint in this.endpoints) {
            const objs = this.endpoints[endpoint];
            objs.forEach((obj) => {
                const verb = obj['verb'];
                const method = obj['method'];
                const action = obj['action'];

                let logic = new logics[endpoint](file_handler, database);
                this.server[method](`/${endpoint}`, logic[action]);
            });
        }

        this.server.listen(this.port, () => {
            console.log('Listening to port', this.port)
        });
    };
};


let file_handler = new storages.FileHandler(settings.file_handler);
let database = new storages.Database(settings.database);

var app = new Application(settings.app, endpoints);
app.run(logics, file_handler, database);
