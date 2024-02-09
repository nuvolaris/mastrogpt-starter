#--web true
#--kind python:default

# from haystack.document_stores.faiss import FAISSDocumentStore

def main(args):
    import os
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai.nuvolaris.io"
    os.environ["OPENAI_API_KEY"] = "05e060f1-4808-404d-b9cf-2fa8e381bf23"
    os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"

    from langchain_community.document_loaders import TextLoader, DirectoryLoader
    loader = DirectoryLoader('.', glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
    splitted_documents = text_splitter.split_documents(documents)
    documents = splitted_documents[0].page_content

    chunks = []
    for document in splitted_documents:
        chunks.append(document.page_content)


    print(type(chunks), len(chunks))
    # documents = [content.page_content for content in splitted_documents]
    
    print("Creating embedding function")
    from langchain_openai import AzureOpenAIEmbeddings
    client = AzureOpenAIEmbeddings()
    # documents = ["Mi chiamo samuele", "Studio openai", "Il cielo è rosso", "QUesta è una frase"]
    embeddings = client.embed_documents(chunks)
    # embeddings = [ (embed, sentence) for embed, sentence in zip (embeddings, documents) ]

    # query = client.embed_query("Di che colore è il cielo?")
    # # print(query)
    print("Created")

    # print("Creating vector storage")
    # import math

    # # Funzione per calcolare la distanza del coseno
    # def cosine_distance(v1, v2):
    #     sumxx, sumxy, sumyy = 0, 0, 0
    #     for i in range(len(v1)):
    #         x = v1[i]; y = v2[i]
    #         sumxx += x*x
    #         sumyy += y*y
    #         sumxy += x*y
    #     return sumxy/math.sqrt(sumxx*sumyy)

    # # Funzione per trovare gli embeddings più simili
    # def get_most_similar_embeddings(embedding_list):
    #     most_similar = None
    #     max_similarity = float('-inf')
    #     sentences = None

    #     for i in range(len(embedding_list)):
    #         for j in range(i+1, len(embedding_list)):
    #             similarity = cosine_distance(embedding_list[i][0], embedding_list[j][0])
    #             if similarity > max_similarity:
    #                 max_similarity = similarity
    #                 most_similar = (embedding_list[i][0], embedding_list[j][0])
    #                 sentences = (embedding_list[i][1], embedding_list[j][1])

    #     return most_similar, sentences
    
    # embeddings.append((query, "Di che colore è il cielo?"))

    # most_similar, sentences = get_most_similar_embeddings(embeddings)

    # print(sentences)

    # query = "Cosa fornisce il framework?"
    # docs = db.similarity_search(query)
    # print(docs[0].page_content)

    res =  {
        "output":  "Ciao. Chiedimi quello che vuoi sui tuoi nodi / pods di Kubernetes.",
        "title": "Titolo di prova",
        "message": "ciaooo"
    }
    return {"body": res}





