import json


def main(arg):
    data = {
        "services": [
            {"name": "Echo", "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/echo"},
            {"name": "Reverse", "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/reverse"},
            {
                "name": "HelloOpenAI",
                "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/hello-openai",
                "parameters": {"name": "OPENAI_API_KEY", "type": "textfield"},
            },
            {
                "name": "HelloKube",
                "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/hello-kube",
                "parameters": {"name": "KUBECONFIG", "type": "textarea"},
            },
        ]
    }
    return {"body": data}
