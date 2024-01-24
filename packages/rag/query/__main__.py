import os
import json
import sys
import logging
from minio import Minio
from io import BytesIO
from haystack.nodes import PDFToTextConverter, PreProcessor
from haystack.document_stores import InMemoryDocumentStore
from openai import OpenAI

# Configura il logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file_from_minio(bucket_name, file_path, minio_client, local_file_name):
    try:
        response = minio_client.get_object(bucket_name, file_path)
        with open(local_file_name, 'wb') as file_data:
            for d in response.stream(32*1024):
                file_data.write(d)
        return local_file_name
    except Exception as e:
        logger.error(f"Errore nel download del file da MinIO: {e}")
        return None

def preprocess_pdf(pdf_file_path):
    converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
    preprocessor = PreProcessor(
        split_by="word",
        split_length=1000,
        split_respect_sentence_boundary=True,
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True
    )

    document = converter.convert(file_path=pdf_file_path, meta=None)
    documents = preprocessor.process(document)
    return " ".join([doc.content for doc in documents])

def query_openai_gpt4(text, api_key):
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key,
        )
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": "You are a knowledgeable assistant who has access only to the following text. Please use this text as your exclusive source of information to answer any questions. Do not reference external content or prior knowledge beyond this text."},
                      {"role": "user", "content": text},
                      {"role": "user", "content": "Spiegami con un sunto in 1000 battute di cosa parla questo documento."}],
            max_tokens=128
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Errore durante la richiesta a OpenAI GPT-4: {e}")
        return "Errore nella richiesta a OpenAI."

def main(params):
    OPENAI_API_KEY = params.get("OPENAI_API_KEY")
    minio_endpoint = params.get("minio_endpoint")
    minio_access_key = params.get("minio_access_key")
    minio_secret_key = params.get("minio_secret_key")
    bucket_name = params.get("bucket_name")
    file_path = params.get("file_path")

    minio_client = Minio(minio_endpoint, access_key=minio_access_key, secret_key=minio_secret_key, secure=True)
    local_pdf_path = "temp_file.pdf"
    pdf_file_path = download_file_from_minio(bucket_name, file_path, minio_client, local_pdf_path)
    if pdf_file_path:
        processed_text = preprocess_pdf(pdf_file_path)
        response = query_openai_gpt4(processed_text, OPENAI_API_KEY)
        os.remove(local_pdf_path)  # Rimuove il file temporaneo
        return response
    else:
        return "Errore nel caricamento del file PDF."

if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        params = {k: v for arg in args for k, v in [arg.split("=")]}
        result = main(params)
        print(result)
    except Exception as e:
        logger.error(f"Errore nell'esecuzione dello script: {e}")
