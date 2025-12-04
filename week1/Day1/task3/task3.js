const fs = require("fs");
const path = require("path");


const logsFilePath = "./logs/day1-sysmetrics.json";
const logs = JSON.parse(fs.readFileSync(logsFilePath, "utf8"));

function logSystemUsage() {
    const cpu = process.cpuUsage();
    const resources = process.resourceUsage();

    const data = {
        logNumber: logs.length,
        timestamp: new Date().toISOString(),
        cpu,
        resources
    };
    
    // Add new log entry
    logs.push(data);

    // Save back to file
    fs.writeFileSync(logsFilePath, JSON.stringify(logs));
}

logSystemUsage();
