#!/usr/bin/env node

const { parseArgs } = require("./helpers/helper.js");
const generateReport = require("./generateReport/generate.js");

async function main() {
    const args = process.argv.slice(2);
    const parsed = parseArgs(args);

    if (!parsed) {
        process.exit(1);
        return;
    }

    const { mapping, unique } = parsed;

    const tasks = [];
    for (const op in mapping) {
        for (const filePath of mapping[op]) {
            tasks.push(generateReport(filePath, op, unique));
        }
    }

    const results = await Promise.all(tasks);
    results.forEach(r => console.log(r));
}

main();