const express = require("express");
const {
  getAllAccounts,
  getPaginatedAccounts,
  getAccountDetails,
  deleteAccountWithId,
  patchAccountWithId,
  postNewAccount
} = require('../controllers/account.js');

const accountRouter = express.Router();

accountRouter.route("/getAll")
  .get(getAllAccounts);

accountRouter.route("/paginated")
  .get(getPaginatedAccounts);

accountRouter.route("/user/:id")
  .get(getAccountDetails)
  .delete(deleteAccountWithId)
  .patch(patchAccountWithId);

accountRouter.route("/new")
  .post(postNewAccount);

module.exports = accountRouter;
