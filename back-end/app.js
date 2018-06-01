"use strict";


let servers = require("./servers");
let routes = require("./routes");
let controllers = require("./controllers");


var restful_server = new servers.RESTfulServer(routes);
restful_server.expose(controllers);
