from  openai import AzureOpenAI

def main(args):
   key = args["OPENAI_KEY"]
   host = args["OPENAI_HOST"]
   AI = AzureOpenAI(api_version="2023-05-15", api_key=key, azure_endpoint=host)

   data = AI.models.list().model_dump()
   models = [m['id'] for m in data['data']]
   return { "models": models }

