import math
from typing import Iterable

from openai import AzureOpenAI
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
import time

import db_manager as dbm



def embedding_fn(input: str | Iterable[str]) -> list[float]:
    azure_client = AzureOpenAI(
        api_key = api_key,
        api_version = "2023-05-15",
        azure_endpoint = endpoint,
    )
    embedding_response = azure_client.embeddings.create(input=input, model="text-embedding-ada-002")
    return [embed.embedding for embed in embedding_response.data]

class EmbeddingManager:
    def __init__(self, embedding_fn) -> None:
        self.embedding_fn = embedding_fn
    
    def _get_chunks_from_documents(self):
        # Loading data
        loader = DirectoryLoader("docs/sdk2", glob="**/*.md", loader_cls=TextLoader)
        documents = loader.load()
        print(*[document.metadata for document in documents], sep="\n")

        # Splitting data
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            strip_headers=False
        )

        chunks = []
        for document in documents:
            md_header_splits = markdown_splitter.split_text(document.page_content)
            chunks.extend( [
                document.page_content for document in md_header_splits
            ])

        print(f"I have to embed {len(chunks)} chunks")
    

    def get_most_similar_embeddings(self, query):
        embed_query = self.azure_client.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding
        most_similar = None
        max_similarity = float("-inf")
        sentence = None
        
        embedding_list = self._load_embeddings()

        for i in range(len(embedding_list)):
            similarity = self._cosine_distance([embed_query[0]], embedding_list[i]['embedding'])
            
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar = embedding_list[i]['embedding']
                sentence = embedding_list[i]['literal']

        return sentence


    def generate_embeddings(self):
        chunks = self._get_chunks_from_documents()

        embeddings = []
        stop, step = len(chunks), 7
        for i in range(0, stop, step):
            # print(f"Started embedding chunks {i}-{i+step} of {stop}")

            chunks_slice = chunks[i : i + step]
            embeddings.extend(  self.embedding_fn(chunks_slice) )
            
            # print(f"Ended embedding chunks {i}-{i+step} of {stop}")
            time.sleep(4)

        # Save the generated embeddings
        dbm.save(embeddings)


    def _load_embeddings(self):
        # Recupera gli oggetti da MongoDB
        objs = dbm.retrive("caep_embeddings_md")
        return objs 

    def _cosine_distance(self, v1, v2):
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)