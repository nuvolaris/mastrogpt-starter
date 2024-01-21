def main(args):
    input = args.get("input", "")
    try:
        # get the state if available
        counter = int(args.get("state")) +1
    except:
        # initialize the state
        counter = 1
    # state is a counter incremented at any invocation
    return {
        "body": {
            "output": "(%d) %s" % (counter, input[::-1]),
            "state": str(counter),
            "message": f"You have inverted {counter} words"
        }
    }