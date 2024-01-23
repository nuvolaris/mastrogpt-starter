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
                "url": "openai/chat",
                "parameters": {
                    "name": "OPENAI_API_KEY",
                    "type": "textfield"
                },
            },
        ]
    }
    return {"body": data}
