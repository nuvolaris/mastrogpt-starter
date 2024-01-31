#--web true
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--param OPENAI_API_HOST $OPENAI_API_HOST
#--param PUBLIC_URL_CALENDAR_ID $PUBLIC_URL_CALENDAR_ID

import urllib.parse
import re
import json


def main(args):
    
    input = args.get("input", "")
    if input == "":
        res = {
                "output": "Welcome to the OpenAI demo chat for google calendar",
                "title": "OpenAI Chat",
                "message": "You can chat with OpenAI and ask to describe your today events on google calendar."
        }
    else :
        res = {
            "output": "click on the button on the right to authenticate",
            "title": "OpenAI Chat",
            "message": generate_authorization_url(args)
        }    
    

    return {"body": res }

def generate_authorization_url(args):
    client_id = args.get('PUBLIC_URL_CALENDAR_ID')
    redirect_uri = 'http://127.0.0.1:5173/calendar'
    scope = 'https://www.googleapis.com/auth/calendar'
    response_type = 'code'

    authorization_url = (
        f'https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&scope={urllib.parse.quote(scope)}&response_type={response_type}'
    )

    output = html_button_from_code(authorization_url)

    return output

def html_button_from_code(code):
    html = f"""
    <h1>Please visit this link to initiate Google authorization</h1>

    <div>
        <a href="{code}">
            <button type="button">Start</button>
        </a>
    </div>
    """
    return html_output(html)

def html_output(text):
    res = {}

    res['html'] = text
    return res

