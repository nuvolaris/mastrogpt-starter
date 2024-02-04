//--web true
//--kind python:default

const htmlCreator = require("html-creator");

function main(args) {
    const hc = new htmlCreator([
        {
            type: "body",
            content: [
                {
                    type: "h1",
                    content: "Hello, world"
                }
            ]
        }
    ])
    return {
        "body": hc.renderHTML()
    }
}