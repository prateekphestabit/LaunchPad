const { saveUniqueLines } = require("../helpers/helper.js");

const countChars = (content) => content.replace(/\s/g, "").length;

const countWords = (content) => {
    if (!content) return 0;
    return content.trim().split(/\s+/).filter(Boolean).length;
};

const countLines = (content, unique = false, filePath = null) => {
    const lines = content.split(/\r?\n/);

    if (!unique) return lines.length;

    const uniqueLines = [...new Set(lines)];
    if (filePath) saveUniqueLines(filePath, uniqueLines);
    return uniqueLines.length;
}

module.exports = {
    countChars,
    countWords,
    countLines
};