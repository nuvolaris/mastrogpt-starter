#--web true
import json

def main(arg):
    data = {
        "services": [
             {
                "name": "CAEP DOCS",
                "url": "openai/assistant"
            },
            # { 
            #     "name": "Demo", 
            #     "url": "mastrogpt/demo",
            # },
            { 
                "name": "Kubernetes", 
                "url": "openai_kubernetes/chat",
            },
            # {
            #     "name": "OpenAI",
            #     "url": "openai/chat"
            # },
           
        ]
    }
    return {"body": data}
