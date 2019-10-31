import boto3
import sys
import os
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
from netCDF4 import Dataset

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading function')
#dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else res,
        'headers': {
            #'Content-Type': 'application/json' if err else 'image/png',
            'Content-Type': 'application/json',
        },
    }

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    # fig.savefig('/tmp/image1.png')
    img_bytes = BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return base64.encodebytes(img_bytes.read()).decode()

def save_fig_to_s3(fig):
    """Turn a matplotlib Figure into Flask response"""
    # fig.savefig('/tmp/image1.png')
    img_bytes = BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)

    s3 = boto3.resource("s3")
    s3_bucket = os.environ['IMAGES_BUCKET']
    print("BUCKET:")
    print(s3_bucket)
    s3_path = os.environ['IMAGES_DIRECTORY'] + '/' + "test.png"
    #s3.Bucket(s3_bucket).put_object(Key=s3_path, Body=img_bytes.read())
    s3.Bucket(s3_bucket).put_object(Key=s3_path, Body=img_bytes.read(), ACL='public-read', ContentType='image/png')

    return s3_path
    
    
def investigate():
    logger.info(os.listdir('/'))
    
    logger.info(os.listdir('/var/lang/lib/python3.7/site-packages'))
    logger.info(os.listdir('/opt/python/lib/python3.7/site-packages'))
    logger.info('{}'.format(sys.path))
    logger.info('TEMPFILES')
    logger.info(os.listdir('/tmp/'))
    logger.info(os.listdir('/tmp/'))

def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    '''
    operation = event['httpMethod']
    if operation == 'GET':
        payload = event['queryStringParameters']
        
        logger.info(payload)
        
        yaxis=[1,2,3,3,4,7,8]
        xaxis = range(len(yaxis))
        
        # Build the plot
        fig, ax = plt.subplots()
        ax.plot(xaxis,yaxis)

        # Stream the resulting image to s3
        img = save_fig_to_s3(fig)


        return respond(None, {'image': img})
        #return respond(None, {'major':sys.version_info[0],'minor':sys.version_info[1]})
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))

