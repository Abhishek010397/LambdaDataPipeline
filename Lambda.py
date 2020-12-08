import boto3
import os
import json
from datetime import datetime, timedelta
''' Global Variable defined for Bucket, Object and Filenames '''
SRC_BUCKET_NAME = '<<Source-Bucket>>'
DST_BUCKET_NAME = '<<Dest-Bucket>>'


def download_s3_file(myfile):
    s3_source = boto3.client('s3')
    s3_source.download_file(SRC_BUCKET_NAME, myfile, '/tmp/'+myfile)


def upload_s3_file(myfile):
    sts = boto3.client('sts')
    sts_result = sts.assume_role(
        RoleArn='<<Role-of-Dest-A/c>>', RoleSessionName='session')
    s3_dest = boto3.client('s3', aws_access_key_id=sts_result['Credentials']['AccessKeyId'],
                           aws_secret_access_key=sts_result['Credentials']['SecretAccessKey'],
                           aws_session_token=sts_result['Credentials']['SessionToken'])
    s3_dest.upload_file('/tmp/'+myfile, DST_BUCKET_NAME, myfile)


def lambda_handler(event, context):
    try:
        print(event)
        myfile = event['Records'][0]['s3']['object']['key']
        print(myfile)
        download_s3_file(myfile)
        upload_s3_file(myfile)
    except Exception as e:
        print(e)
