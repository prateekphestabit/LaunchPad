const MiddlewareLoader = require("./middleware.js");
const RoutesLoader = require("./routes.js");
const AppLoader = require("./app.js");

class Loader {
    async initializeApp(app, PORT) {
        try {
            console.log('Loading App... \n');
            await MiddlewareLoader.loadMiddlewares(app);
            await RoutesLoader.loadRoutes(app);
            await AppLoader.loadApp(app, PORT);
        } catch (error) {
            console.log('Failed To Load', error);
        }
    }
}

module.exports = new Loader();