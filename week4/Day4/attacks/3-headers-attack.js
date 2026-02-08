// Important Security Headers:

// X-Content-Type-Options: nosniff
//     Prevents browser from guessing file types (MIME sniffing)

// 2. X-Frame-Options: DENY    
//     attacker site:
//        underneeth attacker site - invisible iframe with your site loaded inside
//        one click on attacker site = click on your site = clickjacking attack
//     Prevents your site from being embedded in iframes (clickjacking)

// 3. X-XSS-Protection: 1; mode=block
//     Enables browser's XSS filter
//     attacker injects malicious scripts via URL parameters, browser blocks it

// 4. Strict-Transport-Security (HSTS)
//    Forces HTTPS connections
//    will not allow http connections
 
// 5. Content-Security-Policy (CSP)
//    Controls what resources can be loaded
//    external js are blocked, prevents XSS attacks

// How to prevent?

// Use Helmet.js - it sets all these headers automatically!

// Run: node attacks/3-headers-attack.js


const BASE_URL = 'http://localhost:8000';
const ENDPOINT = '/products/getAll';  // Your actual route

async function headersAttack() {
    const response = await fetch('http://localhost:8000/products/getAll');
    
    const securityHeaders = [
        { 
            name: 'X-Content-Type-Options', 
            expected: 'nosniff',
            purpose: 'Prevents MIME sniffing attacks',
            attack: 'Attacker uploads malicious.txt that browser executes as JavaScript'
        },
        { 
            name: 'X-Frame-Options', 
            expected: 'DENY or SAMEORIGIN',
            purpose: 'Prevents clickjacking attacks',
            attack: 'Attacker embeds your site in invisible iframe, tricks users to click'
        },
        { 
            name: 'X-XSS-Protection', 
            expected: '1; mode=block',
            purpose: 'Enables browser XSS filter',
            attack: 'Attacker injects malicious scripts via URL parameters'
        },
        { 
            name: 'Strict-Transport-Security', 
            expected: 'max-age=31536000',
            purpose: 'Forces HTTPS connections',
            attack: 'Man-in-the-middle intercepts HTTP traffic, steals data'
        },
        { 
            name: 'Content-Security-Policy', 
            expected: "default-src 'self'",
            purpose: 'Controls resource loading',
            attack: 'Attacker injects scripts from external domains'
        },
        { 
            name: 'X-Permitted-Cross-Domain-Policies', 
            expected: 'none',
            purpose: 'Controls Flash/PDF access',
            attack: 'Flash/PDF files can make cross-domain requests'
        },
        { 
            name: 'Referrer-Policy', 
            expected: 'no-referrer',
            purpose: 'Controls referrer information',
            attack: 'Sensitive URLs leaked to third parties via referrer header'
        },
    ];
    
    console.log('Security Header Scan Results:');
    console.log('-'.repeat(50));
    
    let missingCount = 0;
    let presentCount = 0;
    
    for (const header of securityHeaders) {
        const value = response.headers.get(header.name);
        if (value) {
            presentCount++;
            console.log(`\n${header.name}: PRESENT`);
            console.log(`   Value: ${value}`);
        } else {
            missingCount++;
            console.log(`\n${header.name}: MISSING!`);
            console.log(`   Purpose: ${header.purpose}`);
            console.log(`   Expected: ${header.expected}`);
            console.log(`   Attack: ${header.attack}`);
        }
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('SCAN RESULTS:');
    console.log(`\tPresent: ${presentCount}/${securityHeaders.length}`);
    console.log(`\tMissing: ${missingCount}/${securityHeaders.length}`);
    
    const score = Math.round((presentCount / securityHeaders.length) * 100);
    console.log(`\tSecurity Score: ${score}%`);
    
    if (missingCount > 0) {
        console.log('\nVULNERABILITY DETECTED:');
        console.log('\tYour server is missing critical security headers!');
        console.log('\tThis exposes users to:');
        console.log('\t\t->Clickjacking attacks');
        console.log('\t\t->XSS (Cross-Site Scripting)');
        console.log('\t\t->MIME sniffing attacks');
        console.log('\t\t->Man-in-the-middle attacks');
        console.log('\n\nFIX: Use Helmet.js middleware');
    }
    
    
}

async function main() {
    await headersAttack();
}

main();
