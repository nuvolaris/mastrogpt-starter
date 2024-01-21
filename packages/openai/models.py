# File: models.py
from  openai import OpenAI

def main(args):
   ai = OpenAI(api_key=args['OPENAI_API_KEY'])
   data = ai.models.list().model_dump()
   models = [m['id'] for m in data['data']]
   return { "models": models }

"""
out = !source .env ; echo $OPENAI_API_KEY
args = { "OPENAI_API_KEY": out[0]}
#print(args)
"""