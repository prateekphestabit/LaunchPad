const express = require("express");
const {
  getAllProducts,
  getProducts,
  getPaginatedProducts,
  getProductDetails,
  deleteProductWithName,
  patchProductWithName,
  softDeleteProductWithName,
  postNewProduct
} = require('../controllers/products.js');

const productRouter = express.Router();

productRouter.route("/getAll")
  .get(getAllProducts);

productRouter.route("/get")
  .get(getProducts);

productRouter.route("/paginated")
  .get(getPaginatedProducts);

productRouter.route("/name/:name")
  .get(getProductDetails)
  .delete(deleteProductWithName)
  .patch(patchProductWithName);

productRouter.route("/softDelete/:name")
  .patch(softDeleteProductWithName);

productRouter.route("/new")
  .post(postNewProduct);

module.exports = productRouter;
