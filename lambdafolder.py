import boto3
import os
import json
from datetime import datetime, timedelta
''' Global Variable defined for Bucket, Object and Filenames '''
SRC_BUCKET_NAME = 'bucket-name'
DEV_DST_BUCKET_NAME = 'bucket-name'
INT_DST_BUCKET_NAME = 'bucket-name'


def download_s3_file(myfile):
    s3_source = boto3.client('s3')
    # Splitting Myfile into different segments,folders and files
    items = myfile.split('/')
    fparent = items[0]
    ffile = items[1]
    folder_name = fparent
    # take the folder with file and save it to '/tmp/file',only files will be saved in /tmp
    s3_source.download_file(
        SRC_BUCKET_NAME, folder_name+'/'+ffile, '/tmp/'+ffile)


def upload_s3_file(myfile):
    accid = [a/c no., a/c no.]
    for acctid in accid:
        sts = boto3.client('sts')
        sts_result = sts.assume_role(
            RoleArn='arn:aws:iam::'+acctid+':role/Role-Name', RoleSessionName='session')
        s3_dest = boto3.client('s3', aws_access_key_id=sts_result['Credentials']['AccessKeyId'],
                               aws_secret_access_key=sts_result['Credentials']['SecretAccessKey'],
                               aws_session_token=sts_result['Credentials']['SessionToken'])
        items = myfile.split('/')
        fparent = items[0]
        ffile = items[1]
        folder_name = fparent
        if acctid == 'a/c no.':
            s3_dest.put_object(Bucket=DEV_DST_BUCKET_NAME,
                               Key=(folder_name+'/'))
            s3_dest.upload_file(
                '/tmp/'+ffile, DEV_DST_BUCKET_NAME, folder_name+'/'+ffile)
        else:
            # Create the folder structure in dest bucket
            s3_dest.put_object(Bucket=INT_DST_BUCKET_NAME,
                               Key=(folder_name+'/'))
            # Upload the file from /tmp with the folder structure
            s3_dest.upload_file(
                '/tmp/'+ffile, INT_DST_BUCKET_NAME, folder_name+'/'+ffile)


def lambda_handler(event, context):
    try:
        print(event)
        myfile = event['Records'][0]['s3']['object']['key']
        print(myfile)
        download_s3_file(myfile)
        upload_s3_file(myfile)
    except Exception as e:
        print(e)
