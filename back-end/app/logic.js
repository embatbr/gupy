'use strict';


let get_image_path = (data) => {
    if(data.image_name == undefined) {
        return null;
    }

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
    this.__create = (batch_payload, response, next) => {
        let batch_values = new Array();

        batch_payload.forEach((payload) => {
            let address = JSON.parse(payload.address);
            batch_values.push({
                candidate: [
                    payload.email,
                    payload.name,
                    get_image_path(payload),
                    payload.birthdate,
                    payload.gender.toUpperCase(),
                    payload.phone,
                    payload.tags
                ],
                address: [
                    payload.email,
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
                professional_experiences: experience_it(JSON.parse(payload.professional_experiences), payload.email),
                educational_experiences: experience_it(JSON.parse(payload.educational_experiences), payload.email)
            });
        });

        database.register_candidate(batch_values)
        .then((_) => {
            batch_payload.forEach((payload) => {
                if(payload.image_data != undefined) {
                    file_handler.save(get_image_path(payload), payload.image_data);
                }
            });

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

        this.__create([body], response, next);
    }

    this.create_batch = (request, response, next) => {
        let body = request.body;

        if(!has_payload(body, response)) {
            return
        }

        let file_path = get_file_path();
        file_handler.save(file_path, body.file_data);
        let [pipezip, jsons, images] = file_handler.read_zip(file_path);

        pipezip.on('close', (d) => {
            file_handler.remove(file_path);

            console.log('jsons:', jsons);
            console.log('images:', images);

            // let batch_payload = new Array();
            // jsons.forEach((json) => {
            //     json.image_data
            // });

            response.send({});
        });
    };
};


module.exports = {
    CandidateLogic: CandidateLogic
};
