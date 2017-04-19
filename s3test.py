import boto3

# Let's use Amazon S3
s3 = boto3.client('s3')

s3.upload_file(
    './data/vision_test.json', 'media.johnkeefe.net', 'vision.json',
    ExtraArgs={'ACL': 'public-read'}
)

