module.exports = (schema, property = "body") => {
  return (req, res, next) => {
    try {
      const validated = schema.parse(req[property])
      req[property] = validated // overwrite dirty data
      next()
    } catch (err) {
      return res.status(400).json({
        error: "Validation failed",
        details: err.errors
      })
    }
  }
}
