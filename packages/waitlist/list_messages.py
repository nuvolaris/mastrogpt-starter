from openai import OpenAI
import time

def main(args):
    global ASSISTANT_ID
    ASSISTANT_ID = args['ASSISTANT_AI_ID']

    openai = OpenAI(
        organization=args.get('ORGANIZATION'),
        api_key=args.get('API_KEY_ASSISTANT_API')
    )

    res = list_last_assistant_thread_messages(args.get('state'), openai)

    return {
            'body': {
            'output': res[0].text.value,
            'state': args.get('state')
            }
    }
   


def list_last_assistant_thread_messages(thread_id, openai, max_attempts=5):
    try:
        response = openai.beta.threads.messages.list(thread_id)

        all_messages = response.data
        assistant_messages = [
            message.content for message in all_messages if message.role == 'assistant']

        last_assistant_message = assistant_messages[0] if assistant_messages else None
        if last_assistant_message:
            return last_assistant_message
        else:
            if max_attempts > 0:
                time.sleep(3)
                return list_last_assistant_thread_messages(thread_id, openai, max_attempts - 1)
            else:
                raise ValueError(
                    'Maximum attempts reached. Unable to retrieve assistant message.')
    except Exception as error:
        print('Error running thread:', error)
        raise error
