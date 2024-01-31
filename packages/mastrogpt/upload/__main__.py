#--kind python:default
#--web true
#--param MINIO_ACCESS_KEY $MINIO_ACCESS_KEY
#--param MINIO_SECRET_KEY $MINIO_SECRET_KEY
#--param MINIO_DATA_BUCKET $MINIO_DATA_BUCKET
#--param MINIO_HOST $MINIO_HOST
#--param MINIO_PORT $MINIO_PORT

from minio import Minio
import base64
import io

def main(args):

    # Recupero le variabili d'ambiente
    access_key = args['MINIO_ACCESS_KEY']
    secret_key = args['MINIO_SECRET_KEY']
    bucket_name = args['MINIO_DATA_BUCKET']
    host = args['MINIO_HOST']
    port = args['MINIO_PORT']

    # Connessione a MinIO
    client = Minio(f"{host}:{port}",
                   access_key=access_key,
                   secret_key=secret_key,
                   secure=False)

    # Dati del file in Base64 e nome del file
    base64_file = args.get('file', '')
    file_name = args.get('filename', '')

    # Decodifica il file da Base64
    file_data = base64.b64decode(base64_file.split(',')[1])

    # Caricamento del file su MinIO
    try:
        client.put_object(bucket_name, file_name, io.BytesIO(file_data), length=len(file_data))
        return {"body": {"status": "File caricato con successo"}}
    except Exception as e:
        return {"body": {"status": "Errore", "details": str(e)}}
