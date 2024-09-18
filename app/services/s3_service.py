import boto3
import os
from app.core.config import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(file_path, object_name):
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, settings.S3_BUCKET_NAME, object_name, ExtraArgs={'ACL': 'public-read'})
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {str(e)}")
        return None
    return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{object_name}"
