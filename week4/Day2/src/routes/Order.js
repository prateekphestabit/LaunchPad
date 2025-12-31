const express = require("express");
const {
  getAllOrders,
  postOrder
} = require("../controllers/order.js");
const orderRouter = express.Router();

orderRouter.route("/")
    .get(getAllOrders)
    .post(postOrder);

module.exports = orderRouter;