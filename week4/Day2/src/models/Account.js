const mongoose = require('mongoose');
const { encrypt } = require('../service/bcrypt');

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

AccountSchema.set(
    'toJSON',
    { 
        virtuals: true,
        versionKey: false,
        transform: (doc, ret) => {
            delete ret.id;
            return ret;
        }
    }
);

AccountSchema.set('toObject', { virtuals: true });

AccountSchema.pre('save', async function (next) {
    if (!this.isModified('password')) return;
    this.password = await encrypt(this.password);
});

AccountSchema.pre('findOneAndUpdate', async function (next) {
    const update = this.getUpdate();

    if (!update || !update.password) return;

    update.password = await encrypt(update.password);

    this.setUpdate(update);
});

const Account = mongoose.model('Account', AccountSchema);
module.exports = Account;
