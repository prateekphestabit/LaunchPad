const express = require('express');
const PORT = 8000;
const app = express();

let counter = 0;

app.get('/ping', (req, res) =>{
    return res.end(JSON.stringify({ timestamp: Date.now() }));
})

app.get('/headers', (req, res) =>{
    return res.end(JSON.stringify(req.headers));
});

app.get('/count', (req, res) =>{
    counter++;
    return res.end(JSON.stringify({ count: counter }));
});

app.listen(8000, () => {
    console.log('server started on port 8000');
});
