#!/usr/bin/env python

import boto3
import datetime
import os
import random
import string

'''
This lambda is meant to invalidate CloudFront cache when
an object in an S3 Origin is updated.
'''
def lambda_handler(event,context):
    # Grab data from environment
    distro = os.environ['Distribution']

    session = boto3.session.Session()
    client = session.client('cloudfront')

    items = [] 
    for obj in event['Records']:
        caller =  datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        items.append('/' + obj['s3']['object']['key'])
    req = client.create_invalidation(
        DistributionId = distro,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': items
            },
        'CallerReference': caller
        }         
    )
    

