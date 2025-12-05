const express = require('express');
const app = express();

const port = 8000;

app.get('/ping', (req, res) => {
  console.log('hello from the server');
  res.send('pong');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
