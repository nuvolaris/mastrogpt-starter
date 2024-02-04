#--web true
#--kind python:default

from markdown import markdown

def main(args):
    text = "# Welcome\n\nHello, *world*."

    return {
        "body": markdown(text)
    } 
