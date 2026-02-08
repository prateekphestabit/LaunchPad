const productRouter = require("../routes/products.js");
const logger = require('./../utils/logger.js');
const authRouter = require('../routes/auth.js');
class RoutesLoader {
    constructor() {
        this.routes = [];
    }

    async loadRoutes(app) {
        logger.info('Mounting Routes...');

        this.routes = [
            { path: '/products', router: productRouter, name: 'Products Router' },
            { path: '/login', router: authRouter, name: 'Auth Router' }
        ];

        this.routes.forEach(({ path, router, name }) => {
            app.use(path, router);
            logger.info(`${name} mounted at: ${path}`);
        });

        logger.info('Routes Mounted... \n');
    }
}

module.exports = new RoutesLoader();