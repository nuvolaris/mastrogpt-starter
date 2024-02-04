//--web true
//--kind nodejs:default

const marked = require("marked");

function main(args) {
    let text = `# Welcome\n\nHello, *world*.`
    return {
        body:  marked.parse(text)
    }
}

module.exports = main