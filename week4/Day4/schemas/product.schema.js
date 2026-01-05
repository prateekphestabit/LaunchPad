const { z } = require("zod")

const productSchema = z
  .object({
    name: z.string().min(2).max(100).trim(),
    price: z.number().positive(),
    category: z.string().min(2).max(50),
    inStock: z.boolean().default(true)
  })
  .strict()

module.exports = productSchema
