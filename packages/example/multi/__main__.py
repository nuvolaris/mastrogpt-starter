#@ web

import hello

def main(args):
    return {
        "body": hello.hello()
    }