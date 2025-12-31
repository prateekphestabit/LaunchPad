const orderRepo = require('../repositories/order.repository');

async function getAllOrders(req, res) {
    const orders = await orderRepo.findAll();
    res.json(orders);
}

async function postOrder(req, res) {
    try {
        const { productName, price, rating, accountId } = req.body;

        if (!accountId) {
            return res.status(400).json({ message: 'accountId is required' });
        }

        const order = await orderRepo.createOrderWithAccountLink(
            { productName, price, rating },
            accountId
        );

        res.status(201).json(order);
    } catch (err) {
        console.error(err);

        if (err.message === 'Account not found') {
            return res.status(404).json({ message: err.message });
        }

        res.status(500).send('Server error');
    }
}

module.exports = {
    getAllOrders,
    postOrder
};
