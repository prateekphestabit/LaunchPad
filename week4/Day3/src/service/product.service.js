const ProductRepository = require('../repositories/product.repository');

class ProductService {
  async getFilteredProducts({ search, minPrice, maxPrice, tags, sortField, sortOrder, includeDeleted, page, limit }) {
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

    if(page && limit){
        const pageNum = Math.max(parseInt(page) || 1, 1);
        const limitNum = Math.min(parseInt(limit) || 10, 100);
        const skip = (pageNum - 1) * limitNum;

        const { products, total } = await ProductRepository.findFilteredPaginated({query, sort, skip, limitNum});

        return { products, total, page: pageNum, limit: limitNum };
    }

    return await ProductRepository.findFiltered({query, sort});
  }
}

module.exports = new ProductService();