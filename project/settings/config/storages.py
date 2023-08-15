from storages.backends.s3boto3 import S3Boto3Storage
import os

class MediaStorage(S3Boto3Storage):
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    location = 'static'
