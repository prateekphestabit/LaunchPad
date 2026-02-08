const express = require("express");
const rootRouter = express.Router();

rootRouter.route("/").get((req, res) => {
  const middleware1Result = res.locals.middleware1;
  res.send(`Hello from the root path /. ${middleware1Result}`);
});

module.exports = rootRouter;
