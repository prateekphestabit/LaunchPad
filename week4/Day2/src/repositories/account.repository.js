const Account = require('../models/Account.js');

class AccountRepository {
    findAll() { return Account.find().populate('orders');}

    async findPaginated({ skip, limit }) {
        const [accounts, total] = await Promise.all([
            Account.find()
                .skip(skip)
                .limit(limit)
                .lean(),
            Account.countDocuments()
        ]);

        return { accounts, total };
    }

    findById(id) {return Account.findById(id).populate('orders');}

    findByEmail(email) {return Account.findOne({ email });}

    create(data) {return Account.create(data);}

    updateById(id, data) {
        return Account.findByIdAndUpdate(id, data, {
            new: true,
            runValidators: true
        });
    }

    deleteById(id) {return Account.findByIdAndDelete(id);}
}

module.exports = new AccountRepository();