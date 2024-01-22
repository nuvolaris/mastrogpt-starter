from google_auth_oauthlib.flow import Flow

def main(args):
    try:
        code = args.get('code')
        
        state = args.get('state')
        scope = args.get('scope')
        print("scope", scope)
        print("state", state)
        print("code", code)

        print('going to obtaint token')
        token = exchange_code_for_token(code, args)
        print('token is', token)
        return {
            "body": {
                "output": "ok",
                "state": state,
                "token": token
            }
        }
    except Exception as e:
        print("an error occurred", e)
        raise e
    
def exchange_code_for_token(code, args):
    web_client_info = {
        "web": {
            "client_id": args.get('CLIENT_ID'),
            "project_id": args.get('PROJECT_ID'),
            "auth_uri": args.get('AUTH_URI'),
            "token_uri": args.get('TOKEN_URI'),
            "auth_provider_x509_cert_url": args.get('AUTH_PROVIDER_X509_CERT_URL'),
            "client_secret": args.get('CLIENT_SECRET'),
            "redirect_uris": args.get('REDIRECT_URIS_0'),
            "javascript_origins": args.get('JAVASCRIPT_ORIGINS_0')
        }  
    }

    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = Flow.from_client_config(
        web_client_info, scopes,
        redirect_uri=args.get('URL_TO_REDIRECT_CALLBACK'))

    token = flow.fetch_token(
        code=code,
    )

    return token
