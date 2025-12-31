const accountRouter = require("../routes/Account.js");
const orderRouter = require("../routes/Order.js");
const logger = require('./../utils/logger.js');
class RoutesLoader {
    constructor() {
        this.routes = [];
    }

    async loadRoutes(app) {
        logger.info('Mounting Routes...');

        this.routes = [
            { path: '/account', router: accountRouter, name: 'Account Router' },
            { path: '/order', router: orderRouter, name: 'Order Router' }
        ];

        this.routes.forEach(({ path, router, name }) => {
            app.use(path, router);
            logger.info(`${name} mounted at: ${path}`);
        });

        logger.info('Routes Mounted... \n');
    }
}

module.exports = new RoutesLoader();