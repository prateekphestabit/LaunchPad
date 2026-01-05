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

    async findFilteredPaginated({query, sort, skip, limitNum}) {
        const [products, total] = await Promise.all([
            Products.find(query)
                .sort(sort)
                .skip(skip)
                .limit(limitNum)
                .lean(),
            Products.countDocuments(query)
        ]);
        return { products, total };
    }

    async findFiltered({query, sort}){
        return await Products.find(query).sort(sort);
    }

    async findByName(name) {return await Products.findOne({ name });}

    async create(data) {return await Products.create(data);}

    async updateByName(name, data) {return await Products.findOneAndUpdate({ name }, data, { new: true });}

    async deleteByName(name) {return await Products.findOneAndDelete({ name });}

    async softDeleteByName(name) {return await Products.findOneAndUpdate({ name }, { deleted: true }, { new: true });}

    async findWithFilters({ search, minPrice, maxPrice, tags, sortField, sortOrder, includeDeleted, page, limit }) {
        
    }
}

module.exports = new ProductRepository();