"use strict";


const _fs = require('fs');
const mkdirp = require('mkdirp');
const _path = require('path');
const pgp = require('pg-promise')({
    capSQL: true
});


let __query_prefix = 'INSERT INTO recruitment.';


function FileHandler() {
    this.save = (file_path, file_data) => {
        mkdirp(_path.dirname(file_path));

        _fs.writeFile(file_path, new Buffer(file_data, 'base64'), (err) => {
            if(err){
                throw err;
            }

            console.log(`File saved in '${file_path}'`);
        });
    };

    this.remove = (file_path) => {
        _fs.unlinkSync(file_path);
    }
};


function Database(settings) {
    this.db = pgp(settings.connection);

    this.register_candidate = (batch_values) => {
        return this.db.tx((t) => {
            let batch = new Array();

            batch_values.forEach((values) => {
                batch.push(
                    t.none(`${__query_prefix}candidates VALUES ($1, $2, $3, $4, $5, $6, $7)`,
                           values.candidate)
                );
                batch.push(
                    t.none(`${__query_prefix}addresses VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
                           values.address)
                );

                let experiences = ['professional_experiences', 'educational_experiences'];

                experiences.forEach((experience) => {
                    values[experience].forEach((experience_details) => {
                        batch.push(t.none(
                            `${__query_prefix}${experience} VALUES ($1, $2, $3, $4, $5, $6)`,
                            experience_details
                        ));
                    });
                });
            });


            return t.batch(batch);
        });
    };
};


module.exports = {
    FileHandler: FileHandler,
    Database: Database
};
