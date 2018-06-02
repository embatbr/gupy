BEGIN;


CREATE SCHEMA recruitment;


-- CREATE TYPE recruitment.brazilian_state AS ENUM ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
--                                      'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
--                                      'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO');

-- CREATE TABLE recruitment.addresses (
--     id SERIAL NOT NULL,

--     state recruitment.brazilian_state NOT NULL,
--     city VARCHAR(255) NOT NULL,
--     neighborhood VARCHAR(255),
--     place_name VARCHAR(255) NOT NULL, -- euivalent to "logradouro"
--     place_number INTEGER,
--     place_complement VARCHAR(255),

--     cep CHAR(9), -- format: ABCDE-FGH

--     latitude NUMERIC(8,6), -- 6 decimal places gives a precision of 4 inches
--     longitude NUMERIC(9,6), -- 6 decimal places gives a precision of 4 inches

--     PRIMARY KEY (id),
--     UNIQUE (state, city, neighborhood, place_name, place_number, place_complement)
-- );


CREATE TYPE recruitment.candidate_gender AS ENUM ('MALE', 'FEMALE');

CREATE TABLE recruitment.candidates (
    name VARCHAR(255) NOT NULL,
    image_path VARCHAR(255) NOT NULL, -- path to image file
    birthdate DATE NOT NULL,
    gender recruitment.candidate_gender NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    -- address_id INTEGER NOT NULL,
    tags jsonb NOT NULL,

    PRIMARY KEY (email)
    -- PRIMARY KEY (email),
    -- FOREIGN KEY (address_id) REFERENCES recruitment.addresses (id)
);


-- CREATE TABLE recruitment.professional_experiences (
--     id SERIAL NOT NULL,

--     company_name VARCHAR(255) NOT NULL,
--     job VARCHAR(255) NOT NULL,
--     start_date DATE NOT NULL,
--     end_date DATE, -- a null value means 'currently employed by the company'
--     description TEXT,

--     candidate_email VARCHAR(254) NOT NULL,

--     PRIMARY KEY (id),
--     FOREIGN KEY (candidate_email) REFERENCES recruitment.candidates (email)
-- );


-- CREATE TABLE recruitment.educational_experiences (
--     id SERIAL NOT NULL,

--     institution_name VARCHAR(255) NOT NULL,
--     title VARCHAR(255), -- a high school may have this field as null
--     start_date DATE NOT NULL,
--     end_date DATE, -- a null value means 'currently employed by the company'

--     candidate_email VARCHAR(254) NOT NULL,

--     PRIMARY KEY (id),
--     FOREIGN KEY (candidate_email) REFERENCES recruitment.candidates (email)
-- );


COMMIT;
