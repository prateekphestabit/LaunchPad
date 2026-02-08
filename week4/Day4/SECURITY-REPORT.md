### schema validation using zod
- controllers/product.schema.js => controllers/products.js/ => postNewProduct


### 1. Flood Attack (Rate Limiting)
Sends 50 rapid requests to overwhelm the server.
- **Fix:** `express-rate-limit`
- **Run:** `node attacks/2-cors-attack.js`

### 2. CORS Attack
Simulates requests from malicious website.
- **Fix:** `cors` middleware with whitelist
- **RUN:** `/home/prateek/Prateek/LaunchPad/week4/Day4Again/attacks/2-cors-attack`
- **Run:** `python3 -m http.server 3000` run on incognito window

### 3. Missing Headers
Scans for security headers that protect against XSS, clickjacking, etc.
- **Fix:** `helmet` middleware

### 4. Large Payload
Sends 5MB+ payloads to crash/slow server.
- **Fix:** `express.json({ limit: '10kb' })`

### 5. Brute Force
Simulates rapid password guessing.
- **Fix:** Strict rate limiting on auth routes
