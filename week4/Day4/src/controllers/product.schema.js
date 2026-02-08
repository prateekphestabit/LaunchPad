const { z } = require("zod");

const ProductZodSchema = z.object({
  name: z
    .string()
    .min(1)
    .max(100)
    .trim(),

  description: z
    .string()
    .max(1000)
    .optional(),

  price: z
    .number()
    .positive(),

  tags: z
    .array(z.string().min(1).max(30))
    .max(10)
    .optional(),
})
.strict();

module.exports = { ProductZodSchema };