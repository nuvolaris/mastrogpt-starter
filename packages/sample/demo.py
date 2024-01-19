def main(args):
    input = args.get("input", "")
    try:
        # get the state if available
        counter = int(args.get("state"))
    except:
        # initialize the state
        counter = 0
    # state is a counter incremented at any invocation
    return {
        "body": {
            "output": "(%d) %s" % (counter, input[::-1]),
            "state": str(counter + 1)
        }
    }