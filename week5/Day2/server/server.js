const express = require('express');
const mongoose = require('mongoose');   
const Text = require('./models/random');
const cors = require('cors');

const app = express();

async function connect(){
    console.log('Connecting to MongoDB...');
    try{
        await mongoose.connect('mongodb://mongo:27017/week5day2');
        console.log('MongoDB connected');
    } catch (err) {
        console.error('MongoDB connection error:', err);
    }
    console.log('MongoDB connection closed');
}

app.use(cors({
  origin: "http://client:3000",
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

connect();

app.get('/', (req, res) => {
    res.end("helllooo");
})

app.post('/data', (req, res) => {
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
    console.log('Server is running on http://server:8000');
});