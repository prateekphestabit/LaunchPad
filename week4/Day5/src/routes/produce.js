const express = require("express");
const { produceNewJob } = require("../controllers/produce");
const produceRouter = express.Router();

produceRouter.post('/', produceNewJob);

module.exports = produceRouter;
