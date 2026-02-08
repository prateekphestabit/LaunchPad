const logger = require('./../utils/logger.js');
const express = require('express');




//============== global rate limiter for all routes ==============
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({ //100 requests per 10 secs from same IP
    windowMs: 10 * 1000,  // 10 seconds
    max: 100,                   // 100 requests per window
    message: 'Too many requests, try again later'
});



//============== CORS configuration ==============
const cors = require('cors');
const corsOptions = {
    // origin: ['http://localhost:3000'], //evil site
    origin: ['http://MySite.com'], //your actual frontend
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
};


//============== Helmet for security headers ==============
const helmet = require('helmet');



//================= Multer for file upload limits ==================== 
const multer = require('multer');
const upload = multer({
    limits: { fileSize: 5 * 1024 * 1024 }  // 5MB max
});


//================= brute-forece attack  ====================
const authLimiter = rateLimit({
    windowMs: 60 * 1000,  // 1 minute
    max: 5,                     // Only 5 attempts!
    message: {
        error: 'Too many login attempts',
        retryAfter: '1 minute'
    },
    // Skip successful logins from counting
    skipSuccessfulRequests: true
});

class MiddlewareLoader {
    async loadMiddlewares(app) {
        logger.info('Loading Middlewares...');
        app.use(express.json({ limit: '10kb' })); //===================== 10kb limit for JSON payloads ==============
        app.use(express.urlencoded({ extended: true, limit: '10kb' })); //10kb limit for URL-encoded payloads ==============
        app.use(limiter); // Applied global rate limiter 
        app.use(cors(corsOptions)); // Applied CORS configuration
        app.use(helmet()); // Applied security headers
        app.use(upload.any()); // Applied file upload limits
        app.use('/login', authLimiter); // Applied brute-force attack protection
        logger.info('All Middlewares Loaded...\n');
    }
}

module.exports = new MiddlewareLoader();