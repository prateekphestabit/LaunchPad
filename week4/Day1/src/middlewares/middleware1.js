const logger = require('./../utils/logger.js');

async function middleware1(req, res, next) {
    logger.info(`Middleware 1 executed on process pid ${process.pid}`);
    res.locals.middleware1 = 'mai middleware1 se attach ho k aya hu';
    next();
}

module.exports = middleware1;
