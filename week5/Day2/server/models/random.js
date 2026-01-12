const mongoose = require('mongoose');

const TextSchema = new mongoose.Schema(
{
    text: { type: String, unique: true },
});

const Texts = mongoose.model('Texts', TextSchema);
module.exports = Texts;
