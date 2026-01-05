const logger = require('./../utils/logger.js');
const express = require('express');

class MiddlewareLoader {
    async loadMiddlewares(app) {
        logger.info('Loading Middlewares...');
        app.use(express.json());
        app.use(express.urlencoded({ extended: true }));
        logger.info('All Middlewares Loaded...\n');
    }
}

module.exports = new MiddlewareLoader();