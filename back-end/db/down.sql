BEGIN;


DROP TABLE recruitment.education;

DROP TABLE recruitment.professional_experiences;

DROP TABLE recruitment.candidates;

DROP TYPE recruitment.candidate_gender;

DROP TABLE recruitment.addresses;

DROP TYPE recruitment.brazilian_state;


DROP SCHEMA recruitment CASCADE;


COMMIT;
