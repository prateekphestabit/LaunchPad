const express = require("express")
const validate = require("../middlewares/validate")
const productSchema = require("../schemas/product.schema")
const { createProduct } = require("../controllers/product.controller")

const router = express.Router()

router.post("/", validate(productSchema), createProduct)

module.exports = router
