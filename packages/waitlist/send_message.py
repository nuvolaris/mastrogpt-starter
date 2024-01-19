from openai import OpenAI

def main(args):
   
    global ASSISTANT_ID
    ASSISTANT_ID = args.get('ASSISTANT_AI_ID')

    openai = OpenAI(
        organization=args.get('ORGANIZATION'),
        api_key=args.get('API_KEY_ASSISTANT_API')
    )

    post_message_on_thread(args['message'], args['state'], openai)
    run_thread(args['state'], openai)

    return {
        'body': {
            'output':'ok',
            'state': args['state']
        }
    }


def post_message_on_thread(message, thread_id, openai):
    try:
        create_thread_resp = openai.beta.threads.messages.create(
            thread_id, role="user", content=message)
        return create_thread_resp
    except Exception as error:
        print('Error creating message on thread:', error)
        raise error


def run_thread(thread_id, openai):
    try:
        run_thread_resp = openai.beta.threads.runs.create(
            thread_id, assistant_id=ASSISTANT_ID)
        return run_thread_resp
    except Exception as error:
        print('Error running thread:', error)
        raise error
