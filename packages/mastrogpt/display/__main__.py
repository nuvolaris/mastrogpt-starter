import chevron
from pathlib import Path

def message(args):
    with open("message.html") as f:
        return chevron.render(f, args)

def main(args):
    out = ""

    # rendering message box
    if "message" in args:
        if not "title" in args:
            args["title"] = "Message"
        out = message(args)

    code = 200 if out != "" else 204
    return {
        "body": out,
        "statusCode": code
    }

