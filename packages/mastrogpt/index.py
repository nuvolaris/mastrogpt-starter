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
                "name": "Kubernetes", 
                "url": "openai_kubernetes/chat",
            },
            {
                "name": "OpenAI",
                "url": "openai/chat"
            },
            {
                "name": "prova",
                "url": "openai/assistant"
            },
        ]
    }
    return {"body": data}
