const express = require('express');
const app = express();
app.use(express.json());
app.route('/').get((req, res) => {
    res.json({ message: 'Hello from Server 2' });
});

app.listen(8000, () => {
    console.log('Server2 is running on port 8000');
});