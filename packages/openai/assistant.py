from openai import OpenAI

def main(args):

    # get params
    AI = OpenAI(
        organization=args.get('ORGANIZATION'),
        api_key=args.get('API_KEY_ASSISTANT_API')
    )
    AID = args.get('ASSISTANT_AI_ID')

    # retrieve state
    state = args.get("state", "")
    if state == "":
        state = AI.beta.threads.create().id
    
    # read input if any
    input = args.get("input", "")
    if input == "":
        return {
            'body': {
                "state": state,
                "display": "assistant.html"
            }
        }
        
    # post the input
    AI.beta.threads.messages.create(state, role="user", content=input)
    
    AI.beta.threads.runs.create(state, assistant_id=AID)
        

    