#--web true
#--kind python:default
#--timeout 300000
#--memory 2048
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--param OPENAI_API_HOST $OPENAI_API_HOST

#--param MONGODB_URL $MONGODB_URL
from pymongo import MongoClient
from openai import AzureOpenAI
import time
import math

from models import DocsAssistant, ConsistentContextChecker
from mastrogpt_wrapper import Response

class Config:
    DO_EMBEDDINGS = False
    TITLE = "CAEP Docs Assistant"

global azure_client, mongodb_client

# Funzione per calcolare la distanza del coseno
def cosine_distance(v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / math.sqrt(sumxx * sumyy)

def get_most_similar_embeddings(embedding_list, query):
    most_similar = None
    max_similarity = float("-inf")
    sentence = None

    for i in range(len(embedding_list)):
        similarity = cosine_distance(query[0], embedding_list[i][0])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = embedding_list[i][0]
            sentence = embedding_list[i][1]

    return most_similar, sentence

def generate_embeddings(args):
    global azure_client, mongodb_client

    # Connessione a MongoDB
    db = mongodb_client.spesce_ferretdb

    # Loading data
    from langchain_community.document_loaders import TextLoader, DirectoryLoader
    loader = DirectoryLoader("docs/sdk2", glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(*[document.metadata for document in documents], sep="\n")

    # Splitting data
    # from langchain.text_splitter import RecursiveCharacterTextSplitter
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
    # splitted_documents = text_splitter.split_documents(documents)
    from langchain.text_splitter import MarkdownHeaderTextSplitter
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

    # chunks = [document.page_content for document in splitted_documents]
    print(f"I have to embed {len(chunks)} chunks")
    # Embedding data
    embeddings = []
    stop, step = len(chunks), 7
    for i in range(0, stop, step):
        print(f"Started embedding chunks {i}-{i+step} of {stop}")
        chunks_slice = chunks[i : i + step]
        result = azure_client.embeddings.create(input=chunks_slice, model="text-embedding-ada-002")
        embeddings.extend([embed.embedding for embed in result.data])
        print(f"Ended embedding chunks {i}-{i+step} of {stop}")
        time.sleep(4)

    # Save embeddings to MongoDB
    for id, embedding in enumerate(embeddings):
        obj = {
            "embedding": embedding,
            "literal": chunks[id] if id < len(chunks) else ""
        }
        db.caep_embeddings_md.insert_one(obj)
    
    print("Saved all to MongoDB")

def load_embeddings(args, query):
    global azure_client, mongodb_client

    # Connessione a MongoDB
    db = mongodb_client.spesce_ferretdb

    # Recupera gli oggetti da MongoDB
    objs = list(db.caep_embeddings_md.find({}))

    # Esegui la query di ricerca per trovare l'embedding più simile
    embed_query = azure_client.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding

    most_similar, sentence = get_most_similar_embeddings(
        [(obj['embedding'], obj['literal']) for obj in objs],
        (embed_query, query)
    )

    # print(f"La risposta a '{query}' è: {sentence}")
    return sentence

def main(args):
    global azure_client, mongodb_client

    azure_client = AzureOpenAI(
        api_key=args["OPENAI_API_KEY"],
        api_version="2023-05-15",
        azure_endpoint=args["OPENAI_API_HOST"],
    )

    assistant = DocsAssistant(args["OPENAI_API_KEY"], args["OPENAI_API_HOST"])



    mongodb_client = MongoClient("mongodb://spesce_ferretdb:BNHskNcs44YM@nuvolaris-mongodb-0.nuvolaris-mongodb-svc.nuvolaris.svc.cluster.local:27017/spesce_ferretdb?connectTimeoutMS=60000&authMechanism=PLAIN")

    
    if Config.DO_EMBEDDINGS:
        generate_embeddings(args)
        return Response("Save embeddings to mongo db")
    
    
    user_query = args.get("input", "")
    if user_query == "":
        return Response("Ciao. Chiedimi quello che ti interessa sapere sulla documentazione.",
                        Config.TITLE,
                        {"message": "Benvenuto nel CAEP DOCS assistant."})
    
    try:
        history = args["state"]["history"] 
        ccc = ConsistentContextChecker(args["OPENAI_API_KEY"], args["OPENAI_API_HOST"])
        
        if ccc.is_consistent(user_query, flatten_history(history)):
            print(f"{user_query =}  is consistent to {history}")
            completion = assistant.reply(
                to_query=user_query,
                with_given_context=flatten_history(history),
            )
            documentation_response = args["state"]["last_documentation"]
        else:
            print(f"{user_query =}  is not consistent to {history }")
            documentation_response = load_embeddings(args, user_query)
            completion = assistant.reply(
                to_query=user_query,
                with_given_context=documentation_response,
                with_history=history
            )
    
    except KeyError:
        print("There is no history")
        documentation_response = load_embeddings(args, user_query)
        completion = assistant.reply(
            to_query=user_query,
            with_given_context=documentation_response
        )
    
    finally:
        #  we only save the last conversation
        #  improve the memory? Keep it till the user changes subject?
        _history =  [
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": completion}
        ]

        return Response(
            completion,
            Config.TITLE,
            {"mdshow": documentation_response.replace('"', '\\"').replace("\n", '\\n')},
            {"history": _history, "last_documentation": documentation_response}
            
        )
    

def flatten_history(history) -> str:
    response = ""
    for message in history:
        response += f'{message["role"]} : {message["content"]}'
    return response
