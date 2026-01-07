const express = require('express');

class MiddlewareLoader {
    async loadMiddlewares(app) {
        console.log('Loading Middlewares...');
        app.use(express.json());
        app.use(express.urlencoded({ extended: true }));
        console.log('All Middlewares Loaded...\n');
    }
}

module.exports = new MiddlewareLoader();