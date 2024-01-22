from google_auth_oauthlib.flow import Flow
import uuid

def main(args):
    
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

    authorization_url, _ = flow.authorization_url(prompt='consent')
    print('authorization_url evaluated', authorization_url)
    return {
        "body": {
            "output": authorization_url,
            "state": str(uuid.uuid4())
        }
    }