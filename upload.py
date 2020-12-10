import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(file_s3, BUCKET_NAME, s3_file):

    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_s3, BUCKET_NAME, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('./vpc.tf', 'lambdabucket-cerebrone', 's3_file')
