#--web true
#--kind python:default

import htmlgenerator as hg

def main(args):
    page = hg.HTML(hg.HEAD(), hg.BODY(hg.H1("Hello, world")))
    return {
        "body": hg.render(page, {})
    }