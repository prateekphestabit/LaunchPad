const { Worker } = require('bullmq');
const connection = require('./config/redis');

const worker = new Worker(
  'myQueue',
  async (job) => {
    console.log(`Processing job ${job.id}`);

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
  console.log(`email sent to: ${job.data.email} job id: ${job.id}`);
});

worker.on('failed', (job, err) => {
  console.error(`there was an error while sending email to ${job.data.email}: job id ${job.id}`, err.message);
});
