import requests
import json

def main(args):
    try:
        counter = int(args['state'])
    except:
        counter = 0
    input = args.get('input', '')

    url = args.get('SLACK_URL')
    headers = {'Content-type': 'application/json'}
    payload = {'text': input}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return {
            'body': {
            'output': 'ok',
            'state': str(counter + 1)
            }
        }
    else:
        return {
            'body': {
            'output': 'ko',
            'state': str(counter + 1)
            }
        }
