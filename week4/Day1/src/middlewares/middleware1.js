const logger = require('./../utils/logger.js');

async function middleware1(req, res, next) {
    logger.info(`Middleware 1 executed on process pid ${process.pid}`);
    next();
}

module.exports = middleware1;
