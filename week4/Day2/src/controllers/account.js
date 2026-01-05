const accountRepo = require('../repositories/account.repository.js');

async function getAllAccounts(req, res) {
    const accounts = await accountRepo.findAll();
    res.json(accounts);
}   

async function getPaginatedAccounts(req, res) {
    try {
        const page = Math.max(parseInt(req.query.page) || 1, 1);
        const limit = Math.min(parseInt(req.query.limit) || 10, 100);
        const skip = (page - 1) * limit;

        const { accounts, total } = await accountRepo.findPaginated({ skip, limit });

        res.json({
            page,
            limit,
            total,
            totalPages: Math.ceil(total / limit),
            data: accounts
        });
    } catch (err) {
        console.error(err);
        res.status(500).send("Server error");
    }
}

async function getAccountDetails(req, res) {
    const account = await accountRepo.findById(req.params.id);
    if (!account) return res.status(404).send("Account not found");
    res.json(account);
}

async function deleteAccountWithId(req, res) {
    const deletedAccount = await accountRepo.deleteById(req.params.id);
    if (!deletedAccount) return res.status(404).send("Account not found");
    res.json({ message: "Account deleted successfully" });
}

async function patchAccountWithId(req, res) {
    const updates = req.body;

    const updatedAccount = await accountRepo.updateById(req.params.id, updates);
    if (!updatedAccount) return res.status(404).send("Account not found");

    res.json(updatedAccount);
}

async function postNewAccount(req, res) {
    try {
        const { firstName, lastName, email, password } = req.body;

        const existing = await accountRepo.findByEmail(email);
        if (existing) {
            return res.status(409).json({
                message: `Account already exists with id ${existing._id}`
            });
        }

        const account = await accountRepo.create({
            firstName,
            lastName,
            email,
            password,
            orders: []
        });

        res.status(201).json({
            message: "Account created successfully",
            accountId: account._id
        });
    } catch (err) {
        console.error(err);
        res.status(500).send("Server error");
    }
}

module.exports = {
    getAllAccounts,
    getPaginatedAccounts,
    getAccountDetails,
    deleteAccountWithId,
    patchAccountWithId,
    postNewAccount
};
