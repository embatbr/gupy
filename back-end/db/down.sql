BEGIN;


DROP TABLE IF EXISTS recruitment.educational_experiences;

DROP TABLE IF EXISTS recruitment.professional_experiences;

DROP TABLE IF EXISTS recruitment.candidates;

DROP TYPE IF EXISTS recruitment.candidate_gender;

DROP TABLE IF EXISTS recruitment.addresses;

DROP TYPE IF EXISTS recruitment.brazilian_state;


DROP SCHEMA IF EXISTS recruitment CASCADE;


COMMIT;
