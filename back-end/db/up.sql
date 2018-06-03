BEGIN;


CREATE SCHEMA recruitment;


CREATE TYPE recruitment.candidate_gender AS ENUM ('MALE', 'FEMALE');

CREATE TABLE recruitment.candidates (
    email VARCHAR(254) NOT NULL,

    name VARCHAR(255) NOT NULL,
    image_path VARCHAR(255), -- path to image file
    birthdate DATE NOT NULL,
    gender recruitment.candidate_gender NOT NULL,
    phone VARCHAR(11) NOT NULL,
    tags jsonb NOT NULL,

    PRIMARY KEY (email)
);


CREATE TYPE recruitment.brazilian_state AS ENUM ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                                     'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                                     'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO');

CREATE TABLE recruitment.addresses (
    candidate_email VARCHAR(254) NOT NULL, -- unusual, but easier to deal with

    state recruitment.brazilian_state NOT NULL,
    city VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255) NOT NULL,
    place_name VARCHAR(255) NOT NULL, -- euivalent to "logradouro"
    place_number INTEGER NOT NULL,
    place_complement VARCHAR(255) NOT NULL,

    cep CHAR(9) NOT NULL, -- format: ABCDE-FGH

    latitude NUMERIC(8,6) NOT NULL, -- 6 decimal places gives a precision of 4 inches
    longitude NUMERIC(9,6) NOT NULL, -- 6 decimal places gives a precision of 4 inches

    PRIMARY KEY (candidate_email)
);


CREATE TABLE recruitment.professional_experiences (
    candidate_email VARCHAR(254) NOT NULL,

    institution_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE, -- a null value means 'not done yet'
    description TEXT,

    PRIMARY KEY (candidate_email, institution_name, title, start_date),
    FOREIGN KEY (candidate_email) REFERENCES recruitment.candidates (email)
);


CREATE TABLE recruitment.educational_experiences (
    candidate_email VARCHAR(254) NOT NULL,

    institution_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE, -- a null value means 'not done yet'
    description TEXT,

    PRIMARY KEY (candidate_email, institution_name, title, start_date),
    FOREIGN KEY (candidate_email) REFERENCES recruitment.candidates (email)
);


COMMIT;
