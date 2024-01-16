import requests
import json


def main(args):
    input = args.get("input", "")

    url = args.get('SLACK_URL')
    headers = {'Content-type': 'application/json'}
    payload = {'text': args.get('text')}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return {"body": "ok!"}
    else:
        return {"body": "ko"}
