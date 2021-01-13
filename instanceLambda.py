import boto3
region = 'us-west-1'
instances = ['<your-instances-id>', 'can be multiple id']
ec2 = boto3.client('ec2', region_name=your_region_name)


def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
