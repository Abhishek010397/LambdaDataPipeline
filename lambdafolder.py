import boto3
import os
import json
from datetime import datetime, timedelta
''' Global Variable defined for Bucket, Object and Filenames '''
SRC_BUCKET_NAME = 'bucket-name'
DEV_DST_BUCKET_NAME = 'bucket-name'
INT_DST_BUCKET_NAME = 'bucket-name'
TST_DST_BUCKET_NAME = 'bucket-name'


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
    sts = boto3.client('sts')
    # DEV
    sts_result_dev = sts.assume_role(
        RoleArn='arn:aws:iam::'+'acctid'+':role/Role-Name', RoleSessionName='session')
    s3_dest_dev = boto3.client('s3', aws_access_key_id=sts_result_dev['Credentials']['AccessKeyId'],
                               aws_secret_access_key=sts_result_dev['Credentials']['SecretAccessKey'],
                               aws_session_token=sts_result_dev['Credentials']['SessionToken'])
    items = myfile.split('/')
    fparent = items[0]
    ffile = items[1]
    folder_name = fparent
    s3_dest_dev.put_object(Bucket=DEV_DST_BUCKET_NAME, Key=(folder_name+'/'))
    s3_dest_dev.upload_file(
        '/tmp/'+ffile, DEV_DST_BUCKET_NAME, folder_name+'/'+ffile)

    # INT
    sts_result_int = sts.assume_role(
        RoleArn='arn:aws:iam::'+'acctid'+':role/Role-Name', RoleSessionName='session')
    s3_dest_int = boto3.client('s3', aws_access_key_id=sts_result_int['Credentials']['AccessKeyId'],
                               aws_secret_access_key=sts_result_int['Credentials']['SecretAccessKey'],
                               aws_session_token=sts_result_int['Credentials']['SessionToken'])
    items = myfile.split('/')
    fparent = items[0]
    ffile = items[1]
    folder_name = fparent
    s3_dest_int.put_object(Bucket=INT_DST_BUCKET_NAME, Key=(folder_name+'/'))
    s3_dest_int.upload_file(
        '/tmp/'+ffile, INT_DST_BUCKET_NAME, folder_name+'/'+ffile)

    # TST
    sts_result_tst = sts.assume_role(
        RoleArn='arn:aws:iam::'+'acctid'+':role/Role-Name', RoleSessionName='session')
    s3_dest_tst = boto3.client('s3', aws_access_key_id=sts_result_tst['Credentials']['AccessKeyId'],
                               aws_secret_access_key=sts_result_tst['Credentials']['SecretAccessKey'],
                               aws_session_token=sts_result_tst['Credentials']['SessionToken'])

    items = myfile.split('/')
    fparent = items[0]
    ffile = items[1]
    folder_name = fparent
    s3_dest_tst.put_object(Bucket=TST_DST_BUCKET_NAME, Key=(folder_name+'/'))
    s3_dest_tst.upload_file(
        '/tmp/'+ffile, TST_DST_BUCKET_NAME, folder_name+'/'+ffile)


def lambda_handler(event, context):
    try:
        print(event)
        myfile = event['Records'][0]['s3']['object']['key']
        print(myfile)
        download_s3_file(myfile)
        upload_s3_file(myfile)
    except Exception as e:
        print(e)
        
        
 ##Remember to Increase the Lam,bda Basic Execution Time to let's say 10 mins,as there are multiple file transfer b/w several a/c's.
