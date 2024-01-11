import openai

def main(args):
    return {
        "body":{
            "output": f"OpenAI {openai.__version__}"
        }
    }