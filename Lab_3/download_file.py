import boto3

s3 = boto3.client('s3')
bucket_name = 'nikhils-unique-bucket-3'
file_name = 'myfile.txt'
download_name = 'downloaded-file.txt'

s3.download_file(bucket_name, file_name, download_name)
print(f'File {file_name} downloaded successfully as {download_name}!')