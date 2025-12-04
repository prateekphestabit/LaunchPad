const { readFileContent, saveUniqueLines, measureMemory, appendPerformanceLog } = require("../helpers/helper.js");
const { countChars, countWords, countLines } = require("../operations/operations.js");

async function generateReport(filePath, operation, unique = false) {
    const startTime = Date.now();
    const startMem = measureMemory();

    const content = await readFileContent(filePath);
    let count = 0;

    if (operation === "chars") count = countChars(content);
    else if (operation === "words") count = countWords(content);
    else if (operation === "lines") {
        if (!unique) {
            count = countLines(content);
        } else {
            const lines = content.split(/\r?\n/);
            const uniqueLines = [...new Set(lines)];
            await saveUniqueLines(filePath, uniqueLines);
            count = uniqueLines.length;
        }
    }

    const endMem = measureMemory();

    const report = {
        file: filePath,
        operation,
        count,
        executionTimeMS: Date.now() - startTime,
        memoryMB: Number(((endMem - startMem) / 1024 / 1024).toFixed(4)),
        timestamp: new Date().toISOString()
    };

    // append to logs/performance.json
    await appendPerformanceLog(report);

    return report;
}

module.exports = generateReport;