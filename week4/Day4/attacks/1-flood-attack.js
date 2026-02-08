async function floodAttack() {
    console.log('Sending 50 concurrent requests to overwhelm the server\n');
    
    const startTime = Date.now();
    let successCount = 0;
    let failCount = 0;
    
    const requests = [];
    for (let i = 1; i <= 101; i++) {
        requests.push( //just pushing the promise to array, not awaiting here to send all requests concurrently
            fetch('http://localhost:8000/products/getAll')
                .then(res => {
                    if (res.ok) successCount++;
                    else failCount++;
                    console.log(`Request ${i}: Status ${res.status}`);
                    return res;
                })
                .catch(err => {
                    failCount++;
                    console.log(`Request ${i}: FAILED - ${err.message}`);
                })
        );
    }
    
    // Await all 101 requests to complete
    try{
        await Promise.all(requests);
        
        const duration = Date.now() - startTime;
        
        console.log('\n')
        console.log('RESULTS:');
        console.log(`   Successful: ${successCount}`);
        console.log(`   Failed/Blocked: ${failCount}`);
        console.log(`   Total time: ${duration}ms`);
        
        if (failCount > 0) {
            console.log('\nPROTECTED:');
            console.log(`   Rate limiter stopped ${failCount} requests!`);
            console.log('   Your server is protected from flood attacks.');
        } else {
            console.log('\nVULNERABILITY DETECTED:');
            console.log('   All 101 requests succeeded without any throttling!');
            console.log('   A real attacker could send THOUSANDS of requests');
            console.log('   to crash your server or make it unresponsive.');
            console.log('\nFIX: Add rate limiting middleware');
        }
    }
    catch (error) {
        console.error('Error during flood attack:', error);
    }
    

    // =====================> fixx <=========================
    //already done in middleware.js

}



async function start() {
    console.log('Testing Flood attack at:', 'http://localhost:8000/products/getAll');
    await floodAttack();
}

start();


