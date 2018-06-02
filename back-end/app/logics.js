"use strict";


function CandidateLogic() {
    this.create = (request, response, next) => {
        console.log('body:', request.body);

        response.send('controller create_candidate() called');
    };

    this.read = (request, response, next) => {
        console.log('params:', request.params);

        response.send('controller read_candidate() called');
    };

    this.update = (request, response, next) => {
        console.log('body:', request.body);

        response.send('controller update_candidate() called');
    };

    this.delete = (request, response, next) => {
        console.log('body:', request.body);

        response.send('controller delete_candidate() called');
    };
};


module.exports = {
    candidate: CandidateLogic
};
