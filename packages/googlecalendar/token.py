import requests

def main(args):

    code=args.get('code')

    client_id = args.get('CLIENT_ID')
    client_secret = args.get('CLIENT_SECRET')
    token_endpoint = 'https://oauth2.googleapis.com/token'

    request_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': args.get('URL_TO_REDIRECT_CALLBACK'),
        'grant_type': 'authorization_code'
    }

    try:
        response = requests.post(token_endpoint, data=request_data)

        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response.get('access_token')

            print('Access Token:', access_token)

            return {
                'body': {
                    'output':'ok',
                    'token': access_token
                }
            }
        else:
            print('Error:', response.text)
            response.raise_for_status()
    except Exception as error:
        print('Error:', error)
        raise error

