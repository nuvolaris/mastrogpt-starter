def main(args):
    try:
        code = args.get('code')
        print("code ")
        print(code)
        state = args.get('state')
        print("state ")
        print(state)
        return {
            "body": {
                "state": state,
                "code": code
            }
        }
    except Exception as e:
        print("an error occurred", e)
        raise e