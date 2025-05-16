import boto3, json

lambda_client = boto3.client('lambda')
response = lambda_client.invoke(
    FunctionName='S3LoggerFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        "Records": [
            {"s3": {"bucket": {"name": "491085404221-cfn-deploy-bucket"}, "object": {"key": "index.html"}}}
        ]
    })
)
print(response['StatusCode'], response['Payload'].read().decode())

