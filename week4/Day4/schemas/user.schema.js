const { z } = require("zod")

const userSchema = z
  .object({
    name: z.string().min(2).max(50).trim(),
    email: z.string().email().toLowerCase(),
    password: z.string().min(8).max(72),
    role: z.enum(["user", "admin"]).default("user")
  })
  .strict() // blocks unknown fields

module.exports = userSchema
