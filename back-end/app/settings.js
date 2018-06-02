"use strict";


module.exports = {
    file_handler: {
        root_path: process.env.PROJECT_ROOT_PATH
    },
    database: {
        connection: {
            host: process.env.DB_HOST || 'localhost',
            port: process.env.DB_PORT || 5432,
            database: process.env.DB_NAME || 'gupy',
            user: process.env.DB_USER || 'gupy',
            password: process.env.DB_PASSWORD || 'gupy'
        }
    },
    app: {
        port: process.env.SERVER_PORT || 8000
    }
};
