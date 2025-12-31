const Order = require('../models/Order');
const Account = require('../models/Account');

class OrderRepository {

    findAll() {return Order.find();}

    async createOrderWithAccountLink(orderData, accountId) {
        // create order
        const order = await Order.create(orderData);

        // link order to account
        const account = await Account.findById(accountId);
        if (!account) {
            throw new Error('Account not found');
        }

        account.orders.push(order._id);
        await account.save();

        return order;
    }
}

module.exports = new OrderRepository();
