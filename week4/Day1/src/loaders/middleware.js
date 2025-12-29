const middleware1 = require("../middlewares/middleware1");
const logger = require('./../utils/logger.js');
class MiddlewareLoader {
    constructor() {
        this.middlewares = [];
    }

    async loadMiddlewares(app) {
        logger.info('Loading Middlewares...');

        this.middlewares = [
            { 
                name: 'middleware1', middleware: middleware1 
            }
        ];

        this.middlewares.forEach(({ name, middleware }) => {
            app.use(middleware);            
        });

        logger.info('All Middlewares Loaded...\n');
    }
}

module.exports = new MiddlewareLoader();