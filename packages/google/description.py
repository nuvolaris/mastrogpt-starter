#--web true
#--kind python:default
#--param OPEN_AI_KEY_CALENDAR $OPEN_AI_KEY_CALENDAR

from openai import OpenAI

ROLE = "You are an assistant that reads calendar events sent by the user and describes them in human terms"
MODEL = "gpt-3.5-turbo"
AI = None

def req(user_input):
    print('user_input is ' + str(user_input))
    return [{"role": "system", "content": ROLE}, 
            {"role": "user", "content": str(user_input)}]

def ask(user_input):
    comp = AI.chat.completions.create(model=MODEL, messages=req(user_input))
    if len(comp.choices) > 0:
        return comp.choices[0].message.content
    return "ERROR"

def main(args):
    print('input is', args.get('input'))
    global AI
    AI = OpenAI(api_key=args.get("OPEN_AI_KEY_CALENDAR"))

    user_input = args.get("input", "")
    output = ask(user_input)

    return {"body": {"output": output}}
