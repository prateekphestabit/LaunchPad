const winston = require('winston');
const path = require('path');

const logger = winston.createLogger({
  level: 'info',
  
  format: winston.format.combine(
    winston.format.timestamp({format: 'yyyy-MM-dd HH:mm:ss'}),
    winston.format.printf(({ timestamp, level, message }) => {
      return `${timestamp} [${level.toUpperCase()}]: ${message}`;
    })
  ),
  
  transports: [
    new winston.transports.File({ 
      filename: path.join(__dirname, '../logs/error.log'),
      level: 'info'
    }),
    new winston.transports.Console(),
  ],
});

module.exports = logger;