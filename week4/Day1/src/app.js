require('dotenv').config({ path: `.env.${process.env.NODE_ENV || 'local'}` });

const Loader = require("./loaders/loader.js")

const express = require('express');
const middleware1 = require("./middlewares/middleware1.js");

const rootRouter = require("./routes/root.js");

const app = express();
app.use("/", middleware1, rootRouter);

Loader.initializeApp(app, process.env.PORT, process.env.DB_URI);
