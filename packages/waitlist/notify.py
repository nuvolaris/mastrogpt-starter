import requests
import json

def main(args):
    try:
        state = (args['state'])
    except:
        state = ''
    input = args.get('input', '')

    url = args.get('SLACK_URL')
    headers = {'Content-type': 'application/json'}
    payload = {'text': input}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return {
            'body': {
            'output': 'ok',
            'state': state
            }
        }
    else:
        return {
            'body': {
            'output': 'ko',
            'state': state
            }
        }
