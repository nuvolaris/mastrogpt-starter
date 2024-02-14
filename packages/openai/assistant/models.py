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
        
    def ask(self, query: str) -> str:
        history = [
            {"role": "system", "content": self.ROLE}, 
            {"role": "user", "content": query}
        ]

        completion = self.azure.chat.completions.create(
            model=MODEL,
            messages=history
        )

        if len(completion.choices) < 0:
            return "Our AI models had problems generating a completion for your query. Please try again later."
        
        return completion.choices[0].message.content
    
    

class ConsistentContextChecker(BaseModel):
    ROLE = """
You will be given two texts: a context and a query.
You must say "YES" if you think you can answer the query with the provided context, "NO" otherwise.
Examples:
("Today the sky is blue, the rose is red and I'm hungry.", "Can I afford this car without any leasing?") -> No
("The attribute XL means Extra Large.", "Does XL mean Super Duper?") -> Yes
"""

    def is_consistent(self, query:str, with_given_context: str):
        response = self.ask( f"( {with_given_context}, {query} ) -> ")

        return response == "Yes" 

