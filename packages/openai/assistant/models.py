#--web false

from openai import AzureOpenAI
from abc import ABC, abstractmethod

MODEL = "gpt-35-turbo"


class BaseModel(ABC):
    ROLE = "generic_role"

    def __init__(self, api_key: str, api_host: str) -> None:
        self.azure = AzureOpenAI(api_version="2023-12-01-preview", 
                                api_key=api_key,
                                azure_endpoint=api_host)
        
    def _ask(self, query: str, more_history = []) -> str:
        history = [
            {"role": "system", "content": self.ROLE}, 
            {"role": "user", "content": query}
        ] + more_history

        completion = self.azure.chat.completions.create(
            model=MODEL,
            messages=history
        )

        if len(completion.choices) < 0:
            return "Our AI models had problems generating a completion for your query. Please try again later."
        
        return completion.choices[0].message.content

class DocsAssistant(BaseModel):
    ROLE = """
You are a documentation assistant. 
Your task involves providing concise answers to user queries, based on the context at hand. 
The user can view this context in a different window, so avoid repeating context details in your responses. 

Remember to keep your responses polite and written in Italian.

"""
    def reply(self, to_query: str, with_given_context: str, with_history = []):
        return self._ask(f"""
            # Context: 
            {with_given_context}
            # Query:
            {to_query}
            # Your response is:
            """, with_history)
        
        
    

class ConsistentContextChecker(BaseModel):
    ROLE = """
In this task, you are provided with two pieces of text - a 'query' and a 'context'.
Your responsibility is to determine if the 'query' can be 'answered' solely based on the 'context' given.
Respond with "YES" if the 'context' contains sufficient information to answer the 'query' accurately.
Respond with "NO" if the 'context' lacks the necessary details to fully answer the 'query'. 
Do not try to guess things or be afraid to say "NO".
Your responses should be in English and restricted to either "YES" or "NO".

For example:
If the 'context' is "Today the sky is blue, the rose is red and I'm hungry." and the 'query' is "Can I afford this car without any leasing?", your response should be "NO".
If the 'context' is "The attribute XL means Extra Large." and the query is "Does XL mean really large?", your response should be "YES".
If the 'context' is "The attribute XL means Extra Large." and the query is "Does XS mean extra small?", your response should be "NO".

"""

    def is_consistent(self, query:str, with_given_context: str):
        response = self._ask( f"context: {with_given_context}, query: {query} ")
        return response in set(["YES", "yes", "Si", "SI"]) 

