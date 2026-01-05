const productRepo = require('../repositories/product.repository.js');
const Product = require('../models/products.js');
async function getAllProducts(req, res) {
    const products = await productRepo.findAll();
    res.json(products);
}

async function getProducts(req, res) {
    try {
        const { search, minPrice, maxPrice, tags, sort, includeDeleted } = req.query;

        let sortField, sortOrder;
        if (sort) {
            [sortField, sortOrder] = sort.split(":");
        }

        const products = await productRepo.findWithFilters({
            search,
            minPrice,
            maxPrice,
            tags,
            sortField,
            sortOrder,
            includeDeleted,
        });

        res.json({
            count: products.length,
            data: products
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Server error" });
    }
}

async function getPaginatedProducts(req, res) {
    try {
        const page = Math.max(parseInt(req.query.page) || 1, 1);
        const limit = Math.min(parseInt(req.query.limit) || 10, 100);
        const skip = (page - 1) * limit;

        const { products, total } = await productRepo.findPaginated({ skip, limit });

        res.json({
            page,
            limit,
            total,
            totalPages: Math.ceil(total / limit),
            data: products
        });
    } catch (err) {
        console.error(err);
        res.status(500).send("Server error");
    }
}

async function getProductDetails(req, res) {
    const product = await productRepo.findByName(req.params.name);
    if (!product) return res.status(404).send("Product not found");
    res.json(product);
}

async function deleteProductWithName(req, res) {
    const deletedProduct = await productRepo.deleteByName(req.params.name);
    if (!deletedProduct) return res.status(404).send("Product not found");
    res.json({ message: "Product deleted successfully" });
}

async function softDeleteProductWithName(req, res) {
    const updatedProduct = await productRepo.softDeleteByName(req.params.name);
    if (!updatedProduct) return res.status(404).send("Product not found");
    res.json({
        message: "Product soft deleted successfully",
        product: updatedProduct
    });
}

async function patchProductWithName(req, res) {
    const updates = req.body;

    const updatedProduct = await productRepo.updateByName(req.params.name, updates);
    if (!updatedProduct) return res.status(404).send("Product not found");

    res.json({
        message: "Product updated successfully",
        product: updatedProduct
    });
}

async function postNewProduct(req, res) {
    try {
        const { name, description, price } = req.body;
       
        const existing = await productRepo.findByName(name);
        if (existing) {
            return res.status(409).json({
                message: `Product already exists with name ${existing.name}`
            });
        }

        const product = await productRepo.create({
            name,
            description,
            price,
        });

        res.status(201).json({
            message: "Product created successfully",
            productId: product.name
        });
    } catch (err) {
        console.error(err);
        res.status(500).send("Server error");
    }
}



module.exports = {
    getAllProducts,
    getProducts,
    getPaginatedProducts,
    getProductDetails,
    deleteProductWithName,
    softDeleteProductWithName,
    patchProductWithName,   
    postNewProduct
};