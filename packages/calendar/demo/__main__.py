from google_auth_oauthlib.flow import Flow
import uuid

def main():
    
    web_client_info = {
       "web": {
            "client_id": "xxx",
            "project_id": "xxx",
            "auth_uri": "xxx",
            "token_uri": "xxx",
            "auth_provider_x509_cert_url": "xxx",
            "client_secret": "xxx",
            "redirect_uris": ["xxx"],
            "javascript_origins": ["xxx"]
        }  
    }


    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = Flow.from_client_config(
        web_client_info, scopes,
        redirect_uri='https://nuvolaris.dev/api/v1/web/antoniopiga/callback/callback')

    authorization_url, _ = flow.authorization_url(prompt='consent')
    print('authorization_url evaluated', authorization_url)
    return {
        "body": {
            "output": authorization_url,
            "state": str(uuid.uuid4())
        }
    }