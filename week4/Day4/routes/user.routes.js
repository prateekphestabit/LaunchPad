const express = require("express")
const validate = require("../middlewares/validate")
const userSchema = require("../schemas/user.schema")
const { createUser } = require("../controllers/user.controller")

const router = express.Router()

router.post("/", validate(userSchema), createUser)

module.exports = router
