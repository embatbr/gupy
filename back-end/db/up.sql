BEGIN;


CREATE SCHEMA recruitment;


CREATE TYPE recruitment.brazilian_states AS ENUM ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES',
                                                  'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR',
                                                  'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
                                                  'SP', 'SE', 'TO');

CREATE TABLE recruitment.addresses (
    id SERIAL NOT NULL,

    state recruitment.brazilian_states NOT NULL,
    city VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255) NOT NULL,
    place_name VARCHAR(255) NOT NULL, -- euivalent to "logradouro"
    place_number VARCHAR(10) NOT NULL, -- may be "S/N" or similar
    place_complement VARCHAR(255) NOT NULL,

    cep CHAR(9) NOT NULL, -- format: ABCDE-FGH

    latitude NUMERIC(8,6) NOT NULL, -- 6 decimal places gives a precision of 4 inches
    longitude NUMERIC(9,6) NOT NULL, -- 6 decimal places gives a precision of 4 inches

    PRIMARY KEY (id)
);


CREATE TYPE recruitment.genders AS ENUM ('FEMALE', 'MALE');

CREATE TABLE recruitment.candidates (
    id SERIAL NOT NULL,

    name VARCHAR(255) NOT NULL,
    image_path VARCHAR(255), -- path to image file
    birthdate DATE NOT NULL,
    gender recruitment.genders NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    tags jsonb NOT NULL,

    address_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    UNIQUE (email),
    FOREIGN KEY (address_id) REFERENCES recruitment.addresses (id)
);


CREATE TYPE recruitment.experience_types AS ENUM ('EDUCATIONAL', 'PROFESSIONAL');

CREATE TABLE recruitment.experiences (
    id SERIAL NOT NULL,

    _type recruitment.experience_types NOT NULL,
    institution_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE, -- a null value means 'not done yet'
    description TEXT,

    candidate_id INTEGER NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (candidate_id) REFERENCES recruitment.candidates (id)
);


GRANT USAGE ON SCHEMA recruitment TO gupy_writer, gupy_reader;
GRANT USAGE ON TYPE recruitment.brazilian_states TO gupy_writer, gupy_reader;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA recruitment TO gupy_writer, gupy_reader;

GRANT SELECT ON ALL TABLES IN SCHEMA recruitment TO gupy_writer, gupy_reader;
GRANT INSERT ON ALL TABLES IN SCHEMA recruitment TO gupy_writer;
GRANT UPDATE ON ALL TABLES IN SCHEMA recruitment TO gupy_writer;
GRANT DELETE ON ALL TABLES IN SCHEMA recruitment TO gupy_writer;


COMMIT;
