#--web true
#--kind python:default

import hello

def main(args):
    return { 
        "body": hello.hello()
    }