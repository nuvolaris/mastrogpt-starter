def main(args):
    try:
        code = args.get('code')
        
        state = args.get('state')
        scope = args.get('scope')
        print("scope", scope)
        print("state", state)
        print("code", code)

        print(state)
        return {
            "body": {
                "output": "ok",
                "state": state,
                "code": code
            }
        }
    except Exception as e:
        print("an error occurred", e)
        raise e