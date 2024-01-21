import json

def main(arg):
    data = {
        "services": [
            { 
                "name": "Demo", 
                "url": "mastrogpt/demo",
                "template": "/mastrogpt/demo.html"
            },
            {
                "name": "Chat",
                "url": "openai/chat",
                "template": "/openai/chat.html",
                "parameters": {
                    "name": "OPENAI_API_KEY",
                    "type": "textfield"
                },
            },
        ]
    }
    return {"body": data}
