"use strict";


const pgp = require('pg-promise')({
    capSQL: true
});


function Database(settings) {
    this.db = pgp(settings.connection);

    this.db.any('SELECT count(*) FROM recruitment.addresses')
      .then((data) => {
        console.log('count:', data);
    })
      .catch((err) => {
        console.log('err:', err);
    });
};


module.exports = {
    Database: Database
};
