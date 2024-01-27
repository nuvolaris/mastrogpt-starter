#--web true
#--kind python:default

from .hello import hello

def main(args):
    return {
        "body": hello()
    }