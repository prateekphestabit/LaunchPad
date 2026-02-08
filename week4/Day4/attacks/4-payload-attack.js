// 1. Memory Exhaustion: 100MB JSON body crashes Node.js
// 2. Database Fill: Store huge data, fill up disk space
// 3. Slow Processing: Large payloads take long to parse
// 4. Billing Attack: If you pay per compute/storage

// Why it works without protection:
// --------------------------------
// Express's default body parser has NO size limit!
// It will try to parse ANY size payload.

// How to prevent?
// ---------------
// Set payload size limits in express.json()

// Run: node attacks/4-payload-attack.js


const BASE_URL = 'http://localhost:8000';
const GET_ENDPOINT = '/products/getAll';  // GET route
const POST_ENDPOINT = '/products/new';    // POST route (your actual route)

async function payloadAttack() {
    const sizes = [
        { size: 1, unit: 'KB', bytes: 1024 },
        { size: 10, unit: 'KB', bytes: 10 * 1024 },
        { size: 100, unit: 'KB', bytes: 100 * 1024 },
        { size: 1, unit: 'MB', bytes: 1024 * 1024 },
        { size: 5, unit: 'MB', bytes: 5 * 1024 * 1024 },
    ];
    
    for (const { size, unit, bytes } of sizes) {
        const largeString = 'X'.repeat(bytes);
        const payload = {
            name: `Attack Product ${size}${unit}`,
            description: largeString,
            price: 999
        };
        
        const payloadSize = JSON.stringify(payload).length;
        console.log(`Sending ${size}${unit} payload (${(payloadSize / 1024).toFixed(0)}KB actual)...`);
        
        try {
            const startTime = Date.now();
            const response = await fetch(`${BASE_URL}${POST_ENDPOINT}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const duration = Date.now() - startTime;
            
            if (response.status === 413) {
                console.log(`   BLOCKED - Status 413 (Payload Too Large) - ${duration}ms`);
            } else if (response.ok) {
                console.log(`   ACCEPTED - Status ${response.status} - ${duration}ms`);
            } else {
                console.log(`   Status ${response.status} - ${duration}ms`);
            }
        } catch (error) {
            console.log(`   ERROR: ${error.message}`);
        }
    }
    
    console.log('ANALYSIS:');
    console.log('   If large payloads were ACCEPTED, your server is vulnerable!');
    
    console.log('\nVULNERABILITY IMPACT:');
    console.log('\t->Memory Exhaustion: Large payloads eat RAM');
    console.log('\t->CPU Overload: Parsing big JSON is expensive');
    console.log('\t->Database Fill: Storing huge documents');
    console.log('\t->Denial of Service: Server becomes unresponsive');
    
    console.log('\nFIX: Set payload size limits');
}

async function main() {
    await payloadAttack();
}

main();
