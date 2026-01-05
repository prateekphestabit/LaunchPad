const helmet = require("helmet")
const cors = require("cors")
const rateLimit = require("express-rate-limit")

const securityMiddleware = (app) => {
  // Security headers
  app.use(helmet())

  // CORS policy (tight)
  app.use(
    cors({
      origin: ["http://localhost:5173"],
      methods: ["GET", "POST"],
      credentials: false
    })
  )

  // Rate limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: "Too many requests, slow down"
  })

  app.use(limiter)
}

module.exports = { securityMiddleware }
