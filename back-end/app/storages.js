"use strict";


const _fs = require('fs');
const mkdirp = require('mkdirp');
const _path = require('path');
const pgp = require('pg-promise')({
    capSQL: true
});


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

    this.register_single_candidate = (values) => {
        return this.db.tx((t) => {
            let batch = [
                t.none('INSERT INTO recruitment.candidates VALUES ($1, $2, $3, $4, $5, $6, $7)',
                       values.candidate),
                t.none('INSERT INTO recruitment.addresses VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
                       values.address)
            ];

            let experiences = ['professional_experiences', 'educational_experiences'];

            experiences.forEach((experience) => {
                values[experience].forEach((xp) => {
                    console.log(xp);

                    batch.push(t.none(
                        `INSERT INTO recruitment.${experience} VALUES ($1, $2, $3, $4, $5, $6)`,
                        xp
                    ));
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
