# --web true
import json


def main(_):
    data = {
        "services": [
            {
                "name": "Ambra",
                "url": "openai/ambra"
            },
            {
                "name": "OpenAI",
                "url": "openai/chat"
            },
            {
<<<<<<< HEAD
                "name": "Wordpress",
                "url": "openai/wordpress"
            },
            {
                "name": "Demo",
                "url": "mastrogpt/demo",
            },
            {
                "name": "Calendar",
                "url": "google/chat"
=======
                "name": "Calendar",
                "url": "openai/chat"
>>>>>>> 8323a69 (refactor: messages calendar reading and html output)
            }
        ]
    }
    return {"body": data}
