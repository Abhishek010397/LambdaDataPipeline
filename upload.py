
import os
import boto3

s3_resource = boto3.resource("s3", region_name="us-east-1")


def upload_objects():
    try:
        bucket_name = "<<Bucket-Name>>"
        root_path = 'C:/<<Path-of-the-folder>>'

        my_bucket = s3_resource.Bucket(bucket_name)

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\", "/")
            directory_name = path.replace(root_path, "test_folder")
            for file in files:
                my_bucket.upload_file(os.path.join(
                    path, file), directory_name+'/'+file)

    except Exception as err:
        print(err)


if __name__ == '__main__':
    upload_objects()
