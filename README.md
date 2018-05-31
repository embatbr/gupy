# Gupy Back-end challenge

Details in the [description file](./DESCRIPTION.md).

## Development

### Stages

#### Stage 1

- Create the endpoints for CRUD (POST, GET, PUT/PATCH and DELETE, maybe?);
- Use a PostgreSQL database for persistency:
    - Open connections simply (no need for connection pools for now).
- Responses in JSON and as structured as possible;
- Code as modular as possible and test the parts separately.

This stage

#### Stage 2

- Improve the Create part of the CRUD with insertion in batch (item 2 of the description):
    - Keep response in JSON, as most logical as possible.

#### Stage 3

- Create a simple front-end (no need for frameworks, I think);
- Use internationalization;
- Show candidates on map:
    - Research and map library (gmaps?);
    - Use QuintoAndar's map visualization as inspiration.

#### Stage 4

- Deploy on Heroku (I never used it).

#### Stage 5

- CD/CI using Travis (I never used it also).

### Technicals

#### HTTP verbs and CRUD

Taken from [http://www.restapitutorial.com/lessons/httpmethods.html](http://www.restapitutorial.com/lessons/httpmethods.html)

| HTTP Verb | CRUD | Entire Collection (e.g. /users) | Specific Item (e.g. /users/{id}) |
|-|-|-|-|
| POST | Create | 201 (Created), 'Location' header with link to /users/{id} containing new ID. | 404 (Not Found), 409 (Conflict) if resource already exists. |
| GET | Read | 200 (OK), list of users. Use pagination, sorting and filtering to navigate big lists. | 200 (OK), single user. 404 (Not Found), if ID not found or invalid. |
| PUT | Update/Replace | 405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection. | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| PATCH | Update/Modify | 405 (Method Not Allowed), unless you want to modify the collection itself. | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| DELETE | Delete | 405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable. | 200 (OK). 404 (Not Found), if ID not found or invalid. |

At least for stage 1 the HTTP verbs and CRUD relation will follow the table above. Only the Update action that must be decided is will be PUT or PATCH.
