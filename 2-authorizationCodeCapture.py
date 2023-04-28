#This function can be used as the redirect URI in Quickbooks. Set-up a lambda function with a public url to trigger. 

import json
import os
import boto3
import requests
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    code = event['queryStringParameters']['code']

    # Save the authorization URL to the S3 bucket
    bucket_name = 'brg-auth'
    folder_name = 'authorization-codes'
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}_authorizationCode.txt"
    authorization_url = f"Date requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \nAuthorization Code: {code}"

    s3.put_object(
        Bucket=bucket_name,
        Key=f"{folder_name}/{file_name}",
        Body=authorization_url
    )

    url = "https://wqt3l4rtvvaseurazw5fcmsr2i0uweqz.lambda-url.us-east-1.on.aws/"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("The request was successful.")
        return {
            'statusCode': 200,
            'body': json.dumps('Authorization successful and saved to S3!')
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps('Authorization was not successful')
        }
