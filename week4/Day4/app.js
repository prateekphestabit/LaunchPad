const express = require("express")
const mongoSanitize = require("express-mongo-sanitize")

const { securityMiddleware } = require("./middlewares/security")

const userRoutes = require("./routes/user.routes")
const productRoutes = require("./routes/product.routes")

const app = express()

// Payload size limit (DoS protection)
app.use(express.json({ limit: "10kb" }))

// Remove $ and . from payloads (NoSQL injection)
app.use(mongoSanitize())

// Helmet, CORS, Rate limit
securityMiddleware(app)


app.use("/api/users", userRoutes)
app.use("/api/products", productRoutes)

app.use((req, res) => {
  res.status(404).json({ error: "Route not found" })
})

module.exports = app
