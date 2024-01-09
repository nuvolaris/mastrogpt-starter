def main(arg):
    return {
        "body": {
            "services": [
                {
                    "name": "Echo",
                    "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/echo"
                },
                {
                    "name": "Reverse",
                    "url": "https://nuvolaris.dev/api/v1/web/dashboard/sample/reverse"
                }
            ]
        }
    }
