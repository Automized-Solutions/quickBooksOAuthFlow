import json
import os
import boto3
import requests
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
AUTH_BUCKET_NAME = 'brg-auth'
REFRESH_TOKEN_OBJECT_KEY = 'refresh_token.json'


def get_most_recent_auth_code():
    folder_name = 'authorization-codes'
    response = s3.list_objects_v2(Bucket=AUTH_BUCKET_NAME, Prefix=folder_name)
    if 'Contents' not in response:
        return None
    sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    most_recent_file = sorted_files[0]
    file_content = s3.get_object(Bucket=AUTH_BUCKET_NAME, Key=most_recent_file['Key'])
    content_lines = file_content['Body'].read().decode('utf-8').split('\n')
    auth_code_line = [line for line in content_lines if "Authorization Code" in line][0]
    auth_code = auth_code_line.split(': ')[1]
    # Add this line to log the authorization code
    #logger.info(f"Authorization code: {auth_code}")
    return auth_code

    


def lambda_handler(event, context):
    code = get_most_recent_auth_code()

    if not code:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'No authorization code found in the S3 bucket.'
            })
        }

    payload = {
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=payload)
    response_json = response.json()
    
    if 'error' in response_json:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Error obtaining access and refresh tokens.',
                'error': response_json['error'],
                'error_description': response_json['error_description']
            })
        }

    access_token = response_json['access_token']
    refresh_token = response_json['refresh_token']

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"refresh-tokens/{REFRESH_TOKEN_OBJECT_KEY}",
        Body=json.dumps({'refresh_token': refresh_token})
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Access and refresh tokens obtained successfully.'
        })
    }
