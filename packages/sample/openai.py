import openai

def main(args):
    return {
        "body": f"OpenAI {openai.__version__}"
    }