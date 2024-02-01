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
import json

def main(args):
    
    # Connection to MinIO
    bucket_name = args['MINIO_DATA_BUCKET']
    client = Minio(f"{args['MINIO_HOST']}:{args['MINIO_PORT']}",
                    access_key=args['MINIO_ACCESS_KEY'],
                    secret_key=args['MINIO_SECRET_KEY'],
                    secure=False) # it is false because it is internal access in http

    # if post, we are uploading
    if args.get('__ow_method',"") == "post":
        # Name and File
        base64_file = args.get('file', '')
        file_name = args.get('filename', '')
        # Uploading
        try:
            file_data = base64.b64decode(base64_file.split(',')[1])
            client.put_object(bucket_name, file_name, io.BytesIO(file_data), length=len(file_data))
            return {"body": "Success"}
        except Exception as e:
            return {"error": str(e)}
    else:
        print(dir(client))
        res = []
        for obj in client.list_objects(bucket_name):
            res.append({"name": obj.object_name, "size": obj.size})
        return {"body": res}
