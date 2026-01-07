const produceJob = require('../jobs/email.job.js');

async function produceNewJob(req, res){
    try {
        const data = req.body;
        if (!data) {
            return res.status(400).json({
                success: false,
                message: 'Data is required in request body'
            });
        }

        const job = await produceJob(data);

        res.status(200).json({
            success: true,
            message: 'Job added to queue successfully',
            jobId: job.id,
            data: job.data
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Failed to add job to queue',
            error: error.message
        });
    }
}

module.exports = {
    produceNewJob
}