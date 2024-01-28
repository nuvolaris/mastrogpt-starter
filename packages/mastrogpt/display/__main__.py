#--web true
#--kind python:default

import chevron
import chess, chess.svg
import traceback

def render(src, args):
    with open(src) as f:
        return chevron.render(f, args)
    
def board(args):
    fen = args['chess']
    try: 
        print(fen)
        board = chess.Board(fen)
        data = {"html": chess.svg.board(board=board) }
        out = render("html.html", data)
    except Exception as e:
        data =  {"title": "Bad Chess Position", "message": str(e)}
        out = render("message.html", data)
        traceback.print_exc()

    return out
    
def main(args):
    out = ""

    if "html" in args:
        out = render("html.html", args)
    elif "code" in args:
        data = {
            "code": args['code'],
            "language": args.get("language", "plain_text")
        }
        out = render("editor.html", data)
    elif "chess" in args:
        out = board(args)
    elif "message" in args:
        if not "title" in args:
            args["title"] = "Message"
        out = render("message.html", args)

    code = 200 if out != "" else 204
    return {
        "body": out,
        "statusCode": code
    }

