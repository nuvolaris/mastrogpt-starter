#--web true
import json

def main(_):
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
                "name": "Wordpress",
                "url": "openai/wordpress"
            },
        ]
    }
    return {"body": data}
