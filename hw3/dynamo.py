import boto3
from botocore.exceptions import ClientError

def initialize_aws_clients():
    """Initialize AWS service clients with error handling"""
    try:
        s3 = boto3.client('s3')
        dynamodb = boto3.client('dynamodb')
        print("AWS clients initialized successfully")
        return s3, dynamodb
    except Exception as e:
        print(f"Error initializing AWS clients: {e}")
        exit(1)

def list_s3_files(s3_client, bucket_name):
    """List all files in an S3 bucket with comprehensive error handling"""
    try:
        # Verify bucket exists and is accessible
        s3_client.head_bucket(Bucket=bucket_name)
        
        print(f"\nAttempting to list files in bucket: {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            print(f"Found {len(response['Contents'])} files:")
            for idx, obj in enumerate(response['Contents'], 1):
                print(f"{idx}. {obj['Key']} (Size: {obj['Size']} bytes)")
        else:
            print("Bucket exists but is empty.")
        return True
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Error: Bucket '{bucket_name}' does not exist")
        elif error_code == '403':
            print(f"Access denied to bucket '{bucket_name}'. Check permissions.")
        else:
            print(f"S3 Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def create_dynamodb_table(dynamodb_client, table_name):
    """Create a DynamoDB table with error handling"""
    try:
        response = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'N'}],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"\nCreating DynamoDB table '{table_name}'...")
        dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully!")
        return True
    except dynamodb_client.exceptions.ResourceInUseException:
        print(f"Table '{table_name}' already exists")
        return True
    except ClientError as e:
        print(f"Error creating table: {e}")
        return False

def insert_dynamodb_item(table_name, item_data):
    """Insert an item into DynamoDB with error handling"""
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        print(f"\nInserting item into table '{table_name}':")
        response = table.put_item(
            Item=item_data,
            ReturnConsumedCapacity='TOTAL'
        )
        print("Item inserted successfully!")
        print(f"Consumed capacity: {response['ConsumedCapacity']['CapacityUnits']} units")
        return True
    except ClientError as e:
        print(f"Error inserting item: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    # Initialize AWS clients
    s3_client, dynamodb_client = initialize_aws_clients()
    
    # Configuration - replace these with your values
    config = {
        's3_bucket': 'hw3-bckt-test',  # Replace with your bucket
        'dynamodb_table': 'TestTable',    # Table name
        'sample_item': {                  # Sample data
            'id': 1,
            'name': 'Sample Item',
            'description': 'This is a test item',
            'timestamp': '2023-01-01T00:00:00Z'
        }
    }
    
    # Execute operations
    list_s3_files(s3_client, config['s3_bucket'])
    create_dynamodb_table(dynamodb_client, config['dynamodb_table'])
    insert_dynamodb_item(config['dynamodb_table'], config['sample_item'])

if __name__ == "__main__":
    main()
