const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema(
{
    deleted: { type: Boolean, default: false },
    name: { type: String, required: true },
    description: { type: String },
    price: { type: Number, required: true },
    tags: { type: [String], default: ["apple", "samsung"] },
}
);

ProductSchema.index({ price: 1 });
ProductSchema.index({ name: 1 });
ProductSchema.index({ description: 1 });


const Products = mongoose.model('Products', ProductSchema);
module.exports = Products;
