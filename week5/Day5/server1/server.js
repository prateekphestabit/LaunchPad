const express = require('express');
const mongoose = require('mongoose');   
const Text = require('./models/random');

const app = express();

async function connect(){
    await mongoose.connect('mongodb://mongo:27017/week5day5');
    console.log('MongoDB connected server1');
}
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

connect();

app.post('/', (req, res) => {
    const data = req.body.text;
    console.log('Received data from client:', data);
    Text.create({ text: data })
    .then(() => {
        console.log('Data saved to DB');
        res.end();
    })
    .catch(error => {
        console.error('Error saving data:', error);
        res.status(500).send('Error saving data');
    });
});

app.listen(8000, () => {
    console.log('Server is running on http://server1:8000');
});