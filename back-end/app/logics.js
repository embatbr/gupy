'use strict';


let get_image_path = (data) => {
    let email_base64 = new Buffer(data.email).toString('base64');
    return `resources/images/${email_base64}-${data.image_name}`;
};


function CandidateLogic(file_handler, database) {

    this.create = (request, response, next) => {
        let body = request.body;

        if(body == null || typeof(body) == undefined) {
            response.send({
                'err': 'Payload is null or undefined'
            });
            return
        }

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
            ]
        })
        .then((data) => {
            file_handler.save(get_image_path(body), body.image_data);

            response.send({
                status: 'success',
                message: 'Candidate successfully registered'
            });
        })
        .catch((err) => {
            response.send({
                status: 'error',
                'message': err
            });
        });
    };
};


module.exports = {
    candidate: CandidateLogic
};
