const produceRouter = require("../routes/produce.js");
const logger = require('./../utils/logger.js');
class RoutesLoader {
    constructor() {
        this.routes = [];
    }

    async loadRoutes(app) {
        logger.info('Mounting Routes...');

        this.routes = [
            { path: '/produce', router: produceRouter, name: 'Producer Router' },
        ];

        this.routes.forEach(({ path, router, name }) => {
            app.use(path, router);
            logger.info(`${name} mounted at: ${path}`);
        });

        logger.info('Routes Mounted... \n');
    }
}

module.exports = new RoutesLoader();