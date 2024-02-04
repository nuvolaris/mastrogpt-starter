#--web true
import json

def main(arg):
    data = {
        "services": [
            { 
                "name": "Demo", 
                "url": "mastrogpt/demo",
            },
            {
                "name": "OpenAI",
                "url": "openai/chat"
            },
            {
                "name": "Calendar",
                "url": "openai/chat"
            }
        ]
    }
    return {"body": data}
