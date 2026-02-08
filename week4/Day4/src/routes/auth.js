const express = require("express");

const authRouter = express.Router();

authRouter.route("/")
    .post((req, res) => {
        if(req.body.password === 'the_actual_password') return res.status(200).send('authorized!!');
        res.status(401).send('unauthorized!!');
    });

module.exports = authRouter;