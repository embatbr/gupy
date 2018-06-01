"use strict";


function CandidateController() {
    this.create = (req, res, next) => {
        res.send('controller create_candidate() called');
    };

    this.read = (req, res, next) => {
        res.send('controller read_candidate() called');
    };

    this.update = (req, res, next) => {
        res.send('controller update_candidate() called');
    };

    this.delete = (req, res, next) => {
        res.send('controller delete_candidate() called');
    };
};


module.exports = {
    candidate: CandidateController // is a new object created for every 'require'?
};
