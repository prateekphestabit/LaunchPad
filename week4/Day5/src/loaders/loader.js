const MiddlewareLoader = require("./middleware.js");
const RoutesLoader = require("./routes.js");
const AppLoader = require("./app.js");
const logger = require('./../utils/logger.js');

class Loader {
    async initializeApp(app, PORT) {
        try {
            logger.info('Loading App... \n');
            await MiddlewareLoader.loadMiddlewares(app);
            await RoutesLoader.loadRoutes(app);
            await AppLoader.loadApp(app, PORT);
        } catch (error) {
            console.error('Failed To Load', error);
        }
    }
}

module.exports = new Loader();