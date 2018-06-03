# Gupy Back-end challenge

Details in the [description file](./DESCRIPTION.md).

OBS: I created a branch **python-attempt**, to redo the challenge in a more suitable language. This will soon be pushed.

## API

### Endpoints

- [X] /candidate
- [ ] /candidates

## Running

In any scenario, the database creation is necessary before running the system. Inside directory *back-end*, just type in the terminal

```
./db/action.sh <ACTION>
```

and choose one of the actions below:

- `create` user and database;
- `drop` user and database;
- `up` and `down` schemas and tables;
- `access` the database (using psql).

To execute the back-end application:

```
npm install # this just need to be executed once
./startup.sh
```

## Development

### Stages

#### Stage 1

- [X] Create the routes for CRUD (POST, GET, PUT and DELETE, respectively) for each endpoint;
- [ ] Create the controllers for CRUD:
    - [X] Create
    - [ ] Read
    - [ ] Update
    - [ ] Delete
- [X] Use a PostgreSQL database for persistency:

This stage

#### Stage 2

- [ ] Improve the Create part of the CRUD with insertion in batch (item 2 of the description):
    - Keep response in JSON, as most logical as possible;
- [X] Use connection pool for the database;

#### Stage 3

- [ ] Create a simple front-end (no need for frameworks, I think);
    - Use internationalization;
- [ ] Show candidates on map:
    - Research and map library (gmaps?);
    - Use QuintoAndar's map visualization as inspiration.

#### Stage 4

- [ ] Deploy on Heroku (I never used it).

#### Stage 5

- [ ] CD/CI using Travis (I never used it also).

### Technicals

#### HTTP verbs and CRUD

Taken from [http://www.restapitutorial.com/lessons/httpmethods.html](http://www.restapitutorial.com/lessons/httpmethods.html)

| HTTP Verb | CRUD | Entire Collection (e.g. /candidates) | Specific Item (e.g. /candidates/{id}) |
|-|-|-|-|
| POST | Create | 201 (Created), 'Location' header with link to /candidates/{id} containing new ID. | 404 (Not Found), 409 (Conflict) if resource already exists. |
| GET | Read | 200 (OK), list of candidates. Use pagination, sorting and filtering to navigate big lists. | 200 (OK), single candidate. 404 (Not Found), if ID not found or invalid. |
| PUT | Update/Replace | 405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection. | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| PATCH | Update/Modify | 405 (Method Not Allowed), unless you want to modify the collection itself. | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| DELETE | Delete | 405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable. | 200 (OK). 404 (Not Found), if ID not found or invalid. |

At least for stage 1 the HTTP verbs and CRUD relation will follow the table above. Only the Update action that must be decided is will be PUT or PATCH.
