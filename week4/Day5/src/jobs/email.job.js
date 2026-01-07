const { Queue } = require('bullmq');
const redisConnection = require('../config/redis.js');
const logger = require('../utils/logger.js');

const myQueue = new Queue('myQueue', {
  connection: redisConnection
});

async function produceJob(data) {
  try {
    const job = await myQueue.add('processJob', {
      email: data.email,
      subject: data.subject,
      body: data.body
    }, 
    {
      attempts: 2,
      backoff: {
        type: 'exponential',
        delay: 2000
      }
    });
      
    logger.info(`Job added to queue with ID: ${job.id}`, { data });
    return job;
  } catch (error) {
    logger.error('Error adding job to queue', { error: error.message });
    throw error;
  }
}

module.exports = produceJob;