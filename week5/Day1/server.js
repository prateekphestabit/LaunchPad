const express = require('express');

const PORT = process.env.PORT || 8000;
const app = express();

app.get("/", (req, res) =>{
   console.log("hellooooo from the docker");
   res.send("hello from the docker");
});

app.listen(PORT, ()=>{
    console.log(`server is listening on port ${PORT}`);
});
