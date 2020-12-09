import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(file_s3, BUCKET_NAME, s3_file):
    sts = boto3.client('sts')
    sts_result = sts.assume_role(
        RoleArn='arn:aws:iam::680763698946:role/EC2S3Access', RoleSessionName='session')
    s3 = boto3.client('s3', aws_access_key_id=sts_result['Credentials']['AccessKeyId'],
                      aws_secret_access_key=sts_result['Credentials']['SecretAccessKey'],
                      aws_session_token=sts_result['Credentials']['SessionToken'])

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


uploaded = upload_to_aws('./vpc.txt', 'lambdabucket-cerebrone', 's3_file')
