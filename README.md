# Gupy Challenge

## Description

1. [ ] Registry of a single candidate (**Create** action from CRUD):
    - [X] POST request to endpoint **/candidate**, carrying a JSON payload;
    - [X] Insert into table **candidates**;
    - [X] Insert into table **addresses**;
    - [X] Insert into table **experiences** (professional and educational).
    - [ ] Save image in a file system and reference it in the database.
2. [ ] Registry of multiple candidates (**Create** action from CRUD):
    - [X] POST request to endpoint **/candidates**, carrying a list of JSONs;
    - [ ] Update payload from previous item to a .zip file;
    - [ ] JSON files (one for each entry) inside the .zip files, as well as photo images.
3. [ ] **Read**, **Update** and **Delete** actions from CRUD:
    - [ ] **Read**
    - [ ] **Update**
    - [ ] **Delete**
4. [ ] Front-end;
5. [ ] Internationalization;
6. [ ] Map visualization;
7. [ ] Deploy on Heroku;
8. [ ] Continuous development using Travis.

## Endpoints

- **/candidate** - deals with single entities;
- **/candidates** - deals with entities in batch.

## Running

Execute the script **startup.sh** on your terminal.

**obs:** ***race condition** issues may be present when running on multiple instances behind a load balancer.*
