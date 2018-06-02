"use strict";


const fs = require('fs');
const pgp = require('pg-promise')({
    capSQL: true
});


function FileHandler(settings) {
    this.root_path = settings.root_path;

    this.save = (path, data, is_base_64) => {
        fs.writeFile(path, new Buffer(data, 'base64'), (err) => {
            if(err){
                throw err;
            }

            console.log(`File saved in '${path}'`);
        });
    };

    this.remove = (path) => {
        fs.unlinkSync(path);
    }
}


function Database(settings) {
    this.db = pgp(settings.connection);
    this.queries = {
        candidates: {
            fields: [
                'name', 'image_path', 'birthdate', 'gender', 'email', 'phone', 'tags'
            ],
            positions: [
                '$1', '$2', '$3', '$4', '$5', '$6', '$7'
            ]
        }
    };

    this.insert = (table, values) => {
        let fields = this.queries[table].fields.join(', ');
        let positions = this.queries[table].positions.join(', ');

        let query = `INSERT INTO recruitment.${table}(${fields}) VALUES (${positions})`;
        console.log(query);

        return this.db.none(query, values);
    };
};


module.exports = {
    FileHandler: FileHandler,
    Database: Database
};
