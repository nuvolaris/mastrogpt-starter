import json

def main(arg):
    data = {
        "services": [
            { 
                "name": "Demo", 
                "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/demo"
            },
            {
                "name": "Chat",
                "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/chat",
                "parameters": {
                    "name": "OPENAI_API_KEY",
                    "type": "textfield"
                },
            },
        ]
    }
    return {"body": data}
