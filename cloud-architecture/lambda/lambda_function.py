import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # If this is an API Gateway HTTP invocation, return a simple message
    if "requestContext" in event:
        logger.info("Invoked via HTTP API")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Hello from your Lambda via HTTP!"})
        }

    # Else assume it’s an S3 event
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key    = event["Records"][0]["s3"]["object"]["key"]
        msg    = f"New file uploaded: {key} in bucket: {bucket}"
        logger.info(msg)
        return {"statusCode": 200, "body": json.dumps(msg)}
    except Exception as e:
        logger.error(f"Error processing S3 event: {e}")
        return {"statusCode": 500, "body": json.dumps(str(e))}

