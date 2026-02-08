## search engine

1. getProducts <controllers/products.js>

    ## two output formats :
    1. paginated
    2. not paginated

    extract all the filters from <req.query>
    # search <main query>
    # minPrice & maxPrice <int values>
    # tags <array of tags>
    # sort {
        sortField: <"price"> 
        sortOrder: <default == ascending(1) else if given("desc"=>-1)>
    }
    # includeDeleted <bool default = fasle>
    # page & limit <paginated>

2. making a query object using these fileters <service/product.service.js>

    # query = { monog db expects query in this format 
        deleted: true,
        
        '$or': [ { name: [Object] }, { description: [Object] } ],
       # dono may se kisi bhe field may mile le aa na using $regex: keyword $options: "i"(uppercase lowercse does not matter for matching)
        <>
        
        price: { '$gte': 1, '$lte': 5 },
        
        tags: { '$in': [ 'apple', 'samsung' ] }
    }

    # sort = {
        "price"(sortFieldName): "desc" ? -1 : 1;
    }

    # findFilteredPaginated (if page and limit is given)
    # else findFiltered

3.1 findFilteredPaginated <repositories/product.repository.js>
   # Products.find(query).sort(sort).skip(skip).limit(limitNum),

3.2 findFiltered <repositories/product.repository.js>
   # Products.find(query).sort(sort);

