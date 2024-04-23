

from .config import DEFAULT_FILE_UPLOAD_DIR
from storages.backends.s3boto3 import S3Boto3Storage
import os

class MediaStorage(S3Boto3Storage):
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    location = f'{DEFAULT_FILE_UPLOAD_DIR}media'

class StaticStorage(S3Boto3Storage):
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    location = f'{DEFAULT_FILE_UPLOAD_DIR}static'