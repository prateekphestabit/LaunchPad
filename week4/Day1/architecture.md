## Src => server.js
   # Entery Point => server.js => use "npm start" to start the servers
   server.js uses clustring to host parallel servers 

   # clustring
                |-------- app.js
                |-------- app.js
    server.js---|-------- app.js
                |-------- app.js
                |-------- app.js


## app.js 
   # NODE_ENV is passes inside the package.json scipts

   # Loader is used here to load every module sequencialy:
    DB => middlewares => routes => Load express app


## Loader.js

   1. Load DB from <loaders/db.js>
       *=> connects to mongo db from <config/DBconnection.js>
    
   2. Load middlewares from <loaders/middleware.js>
       *=> use middleware like urlencode here 
       *=> these middleware will be used before every request
   
   3. Load routes from  <loaders/routes.js>

   4. Load express app from <loaders/app.js>
       *=> running on <http://localhost:3000>

## utils => logger.js
   # just used to log errors or info in a structured way with less code 

## test on post man using 
   # GET request on http://localhost:3000
   # or use curl curl http://localhost:3000