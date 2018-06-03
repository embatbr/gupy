'use strict';


let get_image_path = (data) => {
    let email_base64 = new Buffer(data.email).toString('base64');
    return `resources/images/${email_base64}-${data.image_name}`;
};

let get_file_path = () => {
    let now = Date.now();
    return `resources/downloads/${now}-batch.zip`;
};

let nulify_undef = (x) => x === undefined ? null : x

let experience_it = (experiences, email) => {
    let all_values = new Array();

    experiences.forEach((experience) => {
        all_values.push([
            email,
            experience.institution_name,
            experience.title,
            experience.start_date,
            nulify_undef(experience.end_date),
            nulify_undef(experience.description)
        ]);
    });

    return all_values;
};

let has_payload = (body, response) => {
    if(body == null || typeof(body) == undefined) {
        response.send({
            'err': 'Payload is null or undefined'
        });
        return false;
    }

    return true;
};


function CandidateLogic(file_handler, database) {
    this.__create = (body, response, next) => {
        let address = JSON.parse(body.address);

        database.register_single_candidate({
            candidate: [
                body.email,
                body.name,
                get_image_path(body),
                body.birthdate,
                body.gender.toUpperCase(),
                body.phone,
                body.tags
            ],
            address: [
                body.email,
                address.state,
                address.city,
                address.neighborhood,
                address.place_name,
                address.place_number,
                address.place_complement,
                address.cep,
                address.latitude,
                address.longitude
            ],
            professional_experiences: experience_it(JSON.parse(body.professional_experiences), body.email),
            educational_experiences: experience_it(JSON.parse(body.educational_experiences), body.email)
        })
        .then((data) => {
            file_handler.save(get_image_path(body), body.image_data);

            response.send({
                status: 'success'
            });
        })
        .catch((err) => {
            console.log(err);

            response.send({
                status: 'failure',
                'message': err
            });
        });
    };

    this.create = (request, response, next) => {
        let body = request.body;

        if(!has_payload(body, response)) {
            return
        }

        this.__create(body, response, next);
    }

    this.create_batch = (request, response, next) => {
        let body = request.body;
        console.log(body);

        if(!has_payload(body, response)) {
            return
        }

        let file_path = get_file_path();
        file_handler.save(file_path, body.file_data);

        console.log(file_path);
        response.send({});
    };
};


module.exports = {
    CandidateLogic: CandidateLogic
};
