const fs = require("fs");
const path = require("path");

function resolveFilePath(input) {
    const resolved = path.isAbsolute(input) ? input : path.resolve(process.cwd(), input);
    if (fs.existsSync(resolved)) return resolved;
    console.error(`File not found: ${input}`);
    return null;
}

function parseArgs(args) {
    const mapping = {
        chars: [],
        words: [],
        lines: []
    };

    let unique = false;
    let i = 0;

    while (i < args.length) {
        const cmd = args[i];

        

        if (cmd.startsWith("--")) {
            const op = cmd.slice(2);

            if (op === "unique") {
                unique = true;
                i++;
                continue;
            }
            
            if (!mapping[op]) {
                console.error(`Unknown command: ${cmd}`);
                return null;
            }

            i++;
            while (i < args.length && !args[i].startsWith("--")) {
                const resolved = resolveFilePath(args[i]);
                if (resolved) mapping[op].push(resolved);
                i++;
            }
        } else {
            console.error(`Invalid argument: ${cmd}`);
            return null;
        }
    }

    return { mapping, unique };
}

// replace sync read/write with async versions
const readFileContent = (filePath) => fs.promises.readFile(filePath, "utf8");

async function saveUniqueLines(filePath, uniqueLines) {
    const outDir = path.resolve(process.cwd(), "output");
    await fs.promises.mkdir(outDir, { recursive: true });

    const { name } = path.parse(filePath);
    const outPath = path.join(outDir, `${name}.unique.txt`);

    await fs.promises.writeFile(outPath, uniqueLines.join("\n"), "utf8");
    console.log(`Saved unique lines to: ${outPath}`);
}

const measureMemory = () => process.memoryUsage().heapUsed;

async function appendPerformanceLog(report) {
    const logDir = path.resolve(process.cwd(), "logs");
    await fs.promises.mkdir(logDir, { recursive: true });

    const logPath = path.join(logDir, "performance.json");
    let arr = [];

    try {
        const raw = await fs.promises.readFile(logPath, "utf8");
        if (raw && raw.trim()) arr = JSON.parse(raw);
    } catch (err) {
        if (err.code !== "ENOENT") console.error("Failed to read performance log:", err.message);
       
    }

    arr.push(report);

    try {
        await fs.promises.writeFile(logPath, JSON.stringify(arr, null, 2), "utf8");
    } catch (err) {
        console.error("Failed to write performance log:", err.message);
    }
}

module.exports = {
    parseArgs,
    resolveFilePath,
    readFileContent,
    saveUniqueLines,
    measureMemory,
    appendPerformanceLog
};