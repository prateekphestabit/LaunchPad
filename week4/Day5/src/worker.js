const { Worker } = require('bullmq');
const logger = require('./utils/logger.js');
const connection = require('./config/redis');

const worker = new Worker(
  'myQueue',
  async (job) => {
    logger.info(`Processing job ${job.id}`);

    await new Promise((res) => setTimeout(res, 1000));

    // simulate random failure
    if (Math.random() < 0.3) {throw new Error('SMTP failed');}
  },
  {
    connection,
    concurrency: 5,
  }
);

worker.on('completed', (job) => {
  logger.info(`email sent to: ${job.data.email} job id: ${job.id}`);
});

worker.on('failed', (job, err) => {
  logger.error(`there was an error while sending email to ${job.data.email}: job id ${job.id}`, { error: err.message });
});
