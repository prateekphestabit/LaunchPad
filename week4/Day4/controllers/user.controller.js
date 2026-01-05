exports.createUser = (req, res) => {
  res.status(201).json({
    message: "User created securely",
    data: req.body
  })
}
