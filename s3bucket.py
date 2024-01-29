import boto3

bucket_name = 'sv111bucket'

aws_access_key_id = ''
aws_secret_access_key = ''
aws_default_region = 'eu-north-1'  

s3 = boto3.client('s3')

bucket_name = 'назва бакету : '
s3.create_bucket(Bucket=bucket_name)

response = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]
print("Список бакетів:")
for bucket in buckets:
    print(bucket)

file_name = 'шлях-до-файлу'
object_name = 'Обєкт : '
s3.upload_file(file_name, bucket_name, object_name)

download_path = 'Шлях для збереження : '
s3.download_file(bucket_name, object_name, download_path)

response = s3.list_objects_v2(Bucket=bucket_name)
objects = [obj['Key'] for obj in response['Contents']]
print("Список об'єктів у бакеті:")
for obj in objects:
    print(obj)

s3.delete_object(Bucket=bucket_name, Key=object_name)


