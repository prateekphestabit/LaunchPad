require('dotenv').config({ path: `.env.${process.env.NODE_ENV || 'local'}` });

const express = require('express');
const app = express();



// const rootRouter = require("./routes/root.js");
// const middleware1 = require("./middlewares/middleware1.js");
// // before accessing any route, the request will first go through middleware1, and then it will go to the rootRouter
// app.use("/", middleware1, rootRouter);




const Loader = require("./loaders/loader.js")
Loader.initializeApp(app, process.env.PORT, process.env.DB_URI);
