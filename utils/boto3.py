import os, boto3
from botocore.exceptions import NoCredentialsError

def upload_folder_to_s3(local_folder, s3_bucket, s3_prefix, aws_access_key_id, aws_secret_access_key, aws_session_token=None):
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    try:
        # Walk through the local directory and upload each file
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_folder)
                s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Ensure paths are using forward slashes

                # Upload the file
                s3.upload_file(local_path, s3_bucket, s3_key)

        print(f"Folder '{local_folder}' uploaded to S3://{s3_bucket}/{s3_prefix} successfully.")
        return True
    except NoCredentialsError:
        print("Credentials not available or not valid.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_domain():
    return os.environ.get('AWS_S3_CUSTOM_DOMAIN').lstrip('/').rstrip('/') if os.environ.get('AWS_S3_CUSTOM_DOMAIN') else f'{os.environ.get('AWS_S3_STORAGE_BUCKET_NAME')}.s3.{os.environ.get('AWS_S3_REGION_NAME')}.amazonaws.com'

def s3_upload_file(source, destination, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    # Upload log file to S3
    try:
        extra_args = {'ContentType': 'text/plain', 'CacheControl': 'no-cache'}
        # extra_args = {'ContentType': 'application/json'}
        s3.upload_file(source, bucket_name, destination, ExtraArgs=extra_args)
        # print('Log file uploaded successfully!')
        return {
            'success': True,
            'detail': 'Log file uploaded successfully!',
            'log_file': f'{get_domain()}/{destination}'
        }
    except Exception as e:
        # print('An error occurred while uploading the log file:', e)
        return {
            'success': False,
            'detail': 'An error occurred while uploading the log file.'
        }
        

def check_s3_full_access(access_key_id, secret_access_key, region_name):
    # Initialize the IAM client using provided credentials
    iam_client = boto3.client('iam', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name=region_name)

    try:
        # Get information about the current IAM user
        user_info = iam_client.get_user()
        user_name = user_info['User']['UserName']
        # print(f"Checking IAM credentials for user: {user_name}")

        # Check if the user has full access to S3
        s3_full_access_policy_arn = 'arn:aws:iam::aws:policy/AmazonS3FullAccess'

        # Get the list of attached policies for the user
        attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']

        # Check if the S3 full access policy is attached
        s3_full_access = any(policy['PolicyArn'] == s3_full_access_policy_arn for policy in attached_policies)

        if s3_full_access:
            # print(f"{user_name} has S3 full access.")
            return {
                'success': True,
                'detail': f"The user ({user_name}) has been successfully validated and now has proper access."
            }
        else:
            # print(f"{user_name} does not have S3 full access.")
            return {
                'success': False,
                'detail': f"The user ({user_name}) validation was unsuccessful, and do not have proper access."
            }

    except Exception as e:
        # print(f"Error checking IAM credentials: {e}")
        return {
            'success': False,
            'detail': str(e)
        }