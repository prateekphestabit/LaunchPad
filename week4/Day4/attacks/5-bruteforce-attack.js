// Attacker tries many passwords/tokens rapidly until one works.
// Common on login pages, API keys, reset tokens, etc.

const { urlencoded } = require("express");

// How it works:
// -------------
// 1. Attacker gets username (from data breach, guessing, etc.)
// 2. Uses password list (rockyou.txt has 14 million passwords!)
// 3. Tries each password automatically
// 4. Eventually finds the correct one

// Statistics:
// -----------
// - Top 1000 passwords cover ~90% of accounts
// - Automated tools try 1000+ passwords per minute
// - Without rate limiting, cracking is trivial

// How to prevent?
// ---------------
// 1. STRICT rate limiting on auth routes (5 attempts per 15 min)
// 2. Require strong passwords

// Run: node attacks/5-bruteforce-attack.js

async function bruteforceAttack() {
    // Common passwords
    const commonPasswords = [
        '123456','password','123456789','12345678','12345','qwerty','abc123','password1','password123','1234567',      
        'letmein','admin','welcome','monkey','dragon','master','login','princess','iloveyou','sunshine'
    ];
    
    console.log(`Testing ${commonPasswords.length} common passwords...`);
    console.log('   (In real attack, this would be 10,000+ passwords)\n');
    
    let successCount = 0;
    let blockedCount = 0;
    const startTime = Date.now();
    
    for (let i = 0; i < commonPasswords.length; i++) {
        const password = commonPasswords[i];
        
        try {
            // Simulating login attempt (hitting any endpoint)
            const body = new URLSearchParams();
            body.append('password', password);

            const response = await fetch(`http://localhost:8000/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: body.toString()
            });
            const responseText = await response.text();
            if (response.status === 429) {
                blockedCount++;
                console.log(`Attempt ${i + 1}: "${password}" - (Blocked: ${responseText})`);
            } else {
                successCount++;
                
                console.log(`Attempt ${i + 1}: "${password}" - Allowed (${responseText})`);
            }
        } catch (error) {
            console.log(`Attempt ${i + 1}: "${password}" - Error: ${error.message}`);
        }
    }
    
    const duration = Date.now() - startTime;
    const attemptsPerSecond = Math.round(commonPasswords.length / (duration / 1000));
    

    console.log('BRUTE FORCE RESULTS:');
    console.log(`   Blocked: ${blockedCount}`);
    console.log(`   Allowed: ${successCount}`);
    console.log(`   Time: ${duration}ms`);
    console.log(`   Speed: ${attemptsPerSecond} attempts/second`);
    
    if (successCount > 5) {
        console.log('\nVULNERABILITY DETECTED:');
        console.log('   Too many login attempts were allowed!');
        console.log('   At this rate, attacker can try:');
        console.log(`   • ${attemptsPerSecond * 60} passwords per minute`);
        console.log(`   • ${attemptsPerSecond * 3600} passwords per hour`);
        console.log('   • The entire rockyou.txt in just a few hours!');
    } else {
        console.log('\nRate limiting is working!');
    }
}

async function main() {
    await bruteforceAttack();
}

main();
