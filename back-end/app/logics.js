'use strict';


let get_image_path = (data) => {
    let email_base64 = new Buffer(data.email).toString('base64');
    return `resources/images/${email_base64}-${data.image_name}`;
};


function CandidateLogic(file_handler, database) {
    this.__create_candidate_and_address = (data) => {
        let fields = ['name', 'image_name', 'birthdate', 'gender', 'email', 'phone'];

        fields.forEach((field) => {
            if(typeof(data[field]) !== 'string' || data[field].length === 0) {
                return {
                    success: false,
                    err: `Field ${field} is not a string or has length 0`
                };
            }
        });

        let image_path = get_image_path(data);
        let image_data = data.image_data;
        file_handler.save(image_path, image_data);

        let address = JSON.parse(data.address);

        return database.insert_single(
            'create_profile_and_address',
            [
                data.name,
                image_path,
                data.birthdate,
                data.gender.toUpperCase(),
                data.email,
                data.phone,
                data.tags,
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
        );
    };

    this.__create_professional_experiences = (data, candidate_email) => {
        let professional_experiences = JSON.parse(data);

        let values_list = new Array();
        professional_experiences.forEach((professional_experience) => {
            if(professional_experience.end_date === null)
                professional_experience.end_date = 'NULL'
            else {
                professional_experience.end_date = `'${professional_experience.end_date}'`
            }

            let values = [
                `'${professional_experience.company_name}'`,
                `'${professional_experience.job}'`,
                `'${professional_experience.start_date}'`,
                professional_experience.end_date,
                `'${professional_experience.description}'`,
                `'${candidate_email}'`
            ].join(', ');

            values_list.push(`(${values})`);
        });

        if(values_list.length > 0) {
            return database.insert_multiple(
                'create_professional_experience',
                values_list.join(', ')
            );
        }
    };

    this.__create_educational_experiences = (data, candidate_email) => {
        let educational_experiences = JSON.parse(data);

        let values_list = new Array();
        educational_experiences.forEach((educational_experience) => {
            if(educational_experience.end_date === null)
                educational_experience.end_date = 'NULL'
            else {
                educational_experience.end_date = `'${educational_experience.end_date}'`
            }

            let values = [
                `'${educational_experience.institution_name}'`,
                `'${educational_experience.title}'`,
                `'${educational_experience.start_date}'`,
                educational_experience.end_date,
                `'${candidate_email}'`
            ].join(', ');

            values_list.push(`(${values})`);
        });

        if(values_list.length > 0) {
            return database.insert_multiple(
                'create_educational_experience',
                values_list.join(', ')
            );
        }
    };

    this.create = (request, response, next) => {
        let body = request.body;
        let body_type = typeof(body);

        if(body == null || body_type == undefined) {
            response.send({
                'err': 'Payload is null or undefined'
            });
            return
        }

        this.__create_candidate_and_address(body)
            .then(() => {
            this.__create_professional_experiences(body.professional_experiences, body.email)
                .then(() => {
                    this.__create_educational_experiences(body.educational_experiences, body.email)
                        .then(() => {
                        response.send({
                            'success': 'Candidate successfully registered'
                        });
                    })
                        .catch((err) => {
                        file_handler.remove(get_image_path(body));

                        database.insert_single('rollback', body.email)
                            .then(() => {
                            response.send('ROLLBACK');
                        })
                            .catch((err) => {
                            response.send({
                                'err': err
                            });
                        });
                    });
                })
                .catch((err) => {
                file_handler.remove(get_image_path(body));

                database.insert_single('rollback', body.email)
                    .then(() => {
                    response.send('ROLLBACK');
                })
                    .catch((err) => {
                    console.log(err);
                    response.send({
                        'err': err
                    });
                });
            })
        })
            .catch((err) => {
            file_handler.remove(get_image_path(body));
            response.send({
                'err': err
            });
        });
    };

    this.read = (request, response, next) => {
        console.log('params:', request.params);

        response.send('controller read_candidate() called');
    };

    this.update = (request, response, next) => {
        console.log('body:', request.body);

        response.send('controller update_candidate() called');
    };

    this.delete = (request, response, next) => {
        console.log('body:', request.body);

        response.send('controller delete_candidate() called');
    };
};


module.exports = {
    candidate: CandidateLogic
};
