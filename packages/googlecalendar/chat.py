from openai import OpenAI

ROLE = "You are a an assistant that reads google calendar events and describe them in human terms"
MODEL = "gpt-3.5-turbo"
AI = None

def req(msg):
    return [{"role": "system", "content": ROLE}, 
            {"role": "user", "content": msg}]

def ask(input):
    comp = AI.chat.completions.create(model=MODEL, messages=req(input))
    if len(comp.choices) > 0:
        return comp.choices[0].message.content
    return "ERROR"


def main(args):
    global AI
    AI = OpenAI(api_key=args.get("OPEN_AI_KEY_CALENDAR"))

    input = args.get("input", "")
    output = ask(input)

    return {"body": {"output": output}}
