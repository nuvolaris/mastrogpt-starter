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
                "name": "Reclamo",
                "url": "openai/chat"
            },
            {
                "name": "Reclamo-MistralAI",
                "url": "mastrogpt/mistral"
            },
        ]
    }
    return {"body": data}
