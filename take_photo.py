from __future__ import absolute_import

import io
import os
import sys
import json
import boto3

# Let's use Amazon S3
s3 = boto3.client('s3')


# Imports the Google Cloud client library
from google.cloud import vision

image_file = "./photos/latest.jpg"
json_file = "./data/vision.json"

os.system("raspistill -t 500 -hf -o " + image_file)

# Instantiates a client
vision_client = vision.Client()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    image_file)

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content)

# Performs label detection on the image file
labels = image.detect_labels()
label_list = []

print('Labels:')
for label in labels:
    print(label.description)
    label_list.append(label.description)
    
print(label_list)

#build the object
data = {"labels" : label_list}

# dump it to a file as json
with open(json_file, 'wb') as outfile:
    json.dump(data, outfile)

# upload that file to s3
s3.upload_file(
    './data/vision_test.json', 'media.johnkeefe.net', 'vision.json',
    ExtraArgs={'ACL': 'public-read'}
)



