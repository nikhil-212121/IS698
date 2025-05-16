import boto3

ec2 = boto3.client('ec2')
resp = ec2.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running']}])
for r in resp['Reservations']:
    for inst in r['Instances']:
        print(inst['InstanceId'], inst['InstanceType'], inst['State']['Name'])

