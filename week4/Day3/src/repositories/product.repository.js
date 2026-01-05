const Products = require('../models/products.js');

class ProductRepository {
    async findAll() { return await Products.find(); }

    async findPaginated({ skip, limit }) {
        const [products, total] = await Promise.all([
            Products.find()
                .skip(skip)
                .limit(limit)
                .lean(),
            Products.countDocuments()
        ]);

        return { products, total };
    }

    async findByName(name) {return await Products.findOne({ name });}

    async create(data) {return await Products.create(data);}

    async updateByName(name, data) {return await Products.findOneAndUpdate({ name }, data, { new: true });}

    async deleteByName(name) {return await Products.findOneAndDelete({ name });}

    async softDeleteByName(name) {return await Products.findOneAndUpdate({ name }, { deleted: true }, { new: true });}

    async findWithFilters({ search, minPrice, maxPrice, tags, sortField, sortOrder, includeDeleted }) {
        
        const query = { deleted: false };
        if(includeDeleted === 'true') query.deleted = true; 
        
        let sort = {};

        if (search) {
            query.$or = [
                { name: { $regex: search, $options: "i" } },
                { description: { $regex: search, $options: "i" } }
            ];
        }

        if (minPrice || maxPrice) {
            query.price = {};
            if (minPrice) query.price.$gte = parseInt(minPrice);
            if (maxPrice) query.price.$lte = parseInt(maxPrice);
        }

        if (tags) {
            const tagsArray = tags.split(",");
            query.tags = { $in: tagsArray };
        }

        if (sortField) {
            sort[sortField] = sortOrder === "desc" ? -1 : 1;
        }

        const products = await Products.find(query).sort(sort);
        return products;
    }
}

module.exports = new ProductRepository();