const mongoose = require('mongoose');

const OrderSchema = new mongoose.Schema({
    productName: { type: String, required: true },
    price:       { type: Number, required: true, min: 0 },
    rating:      { type: Number, min: 1, max: 5 },
});

const Order = mongoose.model('Order', OrderSchema);
module.exports = Order;
