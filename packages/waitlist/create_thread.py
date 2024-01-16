from openai import OpenAI

def main(args):
    try:
        counter = int(args['state'])
    except:
        counter = 0
    try:
        client = OpenAI(
            organization=args.get('ORGANIZATION'),
            api_key=args.get('API_KEY_ASSISTANT_API')
        )

        empty_thread = client.beta.threads.create()

        return {
            'body': {
            'output': empty_thread.id,
            'state': str(counter + 1)
            }
        }

    except Exception as e:
        raise f'An error occurred: {e}'
