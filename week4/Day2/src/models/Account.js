const mongoose = require('mongoose');
const Order = require('./Order');

const AccountSchema = new mongoose.Schema(
{
    firstName: { type: String, required: true },
    lastName: { type: String },
    email: { type: String, required: true },
    password: { type: String, required: true },

    orders: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Order'
    }]
}
);

AccountSchema.virtual('fullName').get(function () {
    return this.lastName
        ? `${this.firstName} ${this.lastName}`
        : this.firstName;
});

AccountSchema.virtual('totalOrderAmount').get(function () {
    if (!this.orders || this.orders.length === 0) return 0;

    return this.orders.reduce((sum, order) => {
        return sum + (order.price || 0);
    }, 0);
});

AccountSchema.set('toJSON',
    { 
        virtuals: true,
        versionKey: false,
        transform: (doc, ret) => {
            delete ret.id;
            return ret;
        }
    });
AccountSchema.set('toObject', { virtuals: true });

const Account = mongoose.model('Account', AccountSchema);
module.exports = Account;
