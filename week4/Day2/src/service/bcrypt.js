const bcrypt = require('bcrypt');

async function encrypt(password) {
  const hashedPassword = await bcrypt.hash(password, 10);
  return hashedPassword;
}

async function compare(password, hashedPassword) {
  const isMatch = await bcrypt.compare(password, hashedPassword);
  return isMatch;
}

module.exports = { encrypt, compare };