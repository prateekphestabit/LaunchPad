const express = require("express");
const rootRouter = express.Router();

rootRouter.route("/").get((req, res) => {
  res.send("Hello from the root path /");
});

module.exports = rootRouter;
