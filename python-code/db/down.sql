BEGIN;


DROP TABLE IF EXISTS recruitment.experiences;

DROP TYPE IF EXISTS recruitment.experience_types;

DROP TABLE IF EXISTS recruitment.candidates;

DROP TYPE IF EXISTS recruitment.genders;

DROP TABLE IF EXISTS recruitment.addresses;

DROP TYPE IF EXISTS recruitment.brazilian_states;


DROP SCHEMA IF EXISTS recruitment CASCADE;


COMMIT;
