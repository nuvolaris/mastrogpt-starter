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
from chat import ask_openai

from models import ConsistentContextChecker

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
    # db.drop_collection("caep_embeddings")

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
    mongodb_client = MongoClient("mongodb://spesce_ferretdb:BNHskNcs44YM@nuvolaris-mongodb-0.nuvolaris-mongodb-svc.nuvolaris.svc.cluster.local:27017/spesce_ferretdb?connectTimeoutMS=60000&authMechanism=PLAIN")

    do_embeddings = False
    if do_embeddings:
        generate_embeddings(args)
        return {"body": {"output": "Saved embeddings to MongoDB"}}
    else:
    

        input = args.get("input", "")
    
        if input == "":
            res = {
                "output": "Ciao. Chiedimi quello che ti interessa sapere sulla documentazione.",
                "title": "CAEP DOCS Assistant Chat",
                "message": "Welcome to CAEP DOCS assistant."
            }

        else:
            last_response = args["state"]["last_response"]  if  (
                "state" in args and "last_response" in args["state"] 
            ) else None

            ccc = ConsistentContextChecker(args["OPENAI_API_KEY"], args["OPENAI_API_HOST"])
            is_consistent = ccc.is_consistent(input, last_response)

            print(f"{input =}, {is_consistent = }, {last_response = }")
            if last_response:
                if is_consistent:
                    most_similar_sentence = last_response
                    completion = ask_openai(args, query=input, context=most_similar_sentence)
                else:
                    most_similar_sentence = load_embeddings(args, input)
                    completion = ask_openai(args, query=f"""
#######
HISTORY = {last_response} 
#######
QUERY = {input}                                            
""" , context=most_similar_sentence)

            else:
                most_similar_sentence = load_embeddings(args, input)
                completion = ask_openai(args, query=input, context=most_similar_sentence)
# 
            res = {
                "output": completion,
                "title": "CAEP DOCS Assistant Chat",
                "mdshow": most_similar_sentence.replace('"', '\\"').replace("\n", '\\n'),
                "state":  {
                    "last_response": "Documentation: " + most_similar_sentence + "\nBrief: " + completion + "\nUser:" + input + "\n."
                }
            }

        return {"body": res }



# elif input == "DROPDB":
        
#         mongodb_client.drop_collection("caep_embeddings")
#         res = {
#             "output": "Done. Collection has been dropped.",
#             "title": "CAEP DOCS Assistant Chat",
#             "mdshow": "👍🏻"
#         }