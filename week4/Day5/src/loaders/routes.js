const produceRouter = require("../routes/produce.js");
class RoutesLoader {
    constructor() {
        this.routes = [];
    }

    async loadRoutes(app) {
        console.log('Mounting Routes...');

        this.routes = [
            { path: '/produce', router: produceRouter, name: 'Producer Router' },
        ];

        this.routes.forEach(({ path, router, name }) => {
            app.use(path, router);
            console.log(`${name} mounted at: ${path}`);
        });

        console.log('Routes Mounted... \n');
    }
}

module.exports = new RoutesLoader();