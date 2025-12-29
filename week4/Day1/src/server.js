const cluster = require('node:cluster');
const cpuNum = require('node:os').cpus().length;

if (cluster.isPrimary) for (let i = 0; i < cpuNum; i++) cluster.fork();
else {
  require('./app.js')
}