'use strict';


function CandidateLogic(file_handler, database) {
    this.__create = (data) => {
        let fields = ['name', 'image_name', 'birthdate', 'gender', 'email', 'phone'];

        fields.forEach((field) => {
            if(typeof(data[field]) !== 'string' || data[field].length === 0) {
                return {
                    success: false,
                    err: `Field ${field} is not a string or has length 0`
                };
            }
        });

        let email_base64 = new Buffer(data.email).toString('base64');
        let image_path = `resources/images/${email_base64}-${data.image_name}`;
        let image_data = data.image_data;
        file_handler.save(image_path, image_data);

        let values = [
            data.name,
            image_path,
            data.birthdate,
            data.gender.toUpperCase(),
            data.email,
            data.phone,
            data.tags
        ];

        console.log(data.tags);

        return database.insert('candidates', values);
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

        this.__create(body)
            .then(() => {
            response.send({
                'success': 'Candidate successfully registered'
            });
        })
            .catch((err) => {
                console.log(err);
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
