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
        create_profile_and_address: `BEGIN;

WITH address_row AS (
    INSERT INTO
        recruitment.addresses (
            state,
            city,
            neighborhood,
            place_name,
            place_number,
            place_complement,
            cep,
            latitude,
            longitude
        )
    VALUES (
        $8,
        $9,
        $10,
        $11,
        $12,
        $13,
        $14,
        $15,
        $16
    )
    RETURNING id
)
INSERT INTO
    recruitment.candidates (
        name,
        image_path,
        birthdate,
        gender,
        email,
        phone,
        address_id,
        tags
    )
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    (SELECT id FROM address_row),
    $7
);

COMMIT;`,
        create_professional_experience: `INSERT INTO
    recruitment.professional_experiences (
        company_name,
        job,
        start_date,
        end_date,
        description,
        candidate_email
    )
VALUES
`,
        create_educational_experience: `INSERT INTO
    recruitment.educational_experiences (
        institution_name,
        title,
        start_date,
        end_date,
        candidate_email
    )
VALUES
`,
        rollback: `BEGIN;

DELETE FROM
    recruitment.educational_experiences
WHERE
    candidate_email = $1;

DELETE FROM
    recruitment.professional_experiences
WHERE
    candidate_email = $1;

WITH deleted_candidate AS (
    DELETE FROM
        recruitment.candidates
    WHERE
        email = $1
    RETURNING address_id
)
DELETE FROM
    recruitment.addresses
WHERE
    id = (
        SELECT
            address_id
        FROM
            deleted_candidate
    );

COMMIT;
`
    };

    this.insert_single = (action, values) => {
        return this.db.none(this.queries[action], values);
    };

    this.insert_multiple = (action, values) => {
        let query = `${this.queries[action]} ${values}`

        return this.db.none(query);
    };
};


module.exports = {
    FileHandler: FileHandler,
    Database: Database
};
