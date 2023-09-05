import json
import os
import datetime
import boto3

def receive_new_messages():
    # Create SQS client
    sqs = boto3.client('sqs')

    # Get the URL of the SQS Queue
    queue_url = os.getenv('queue-url')

    # Receive messages from the SQS Queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # adjust the number of messages to receive as desired
        WaitTimeSeconds=20  # adjust the wait time as desired
    )

    # Get the messages from the response
    messages = response.get('Messages', [])

    return messages


def lambda_handler(event, context):
    # Get the new messages from the SQS Queue
    records = receive_new_messages()
    
    for record in records:
        message = record['Body']
        
        # Create S3 client
        s3 = boto3.client('s3')

        # Create time variables
        current_time = datetime.datetime.now()
        current_date = datetime.date.today()
        
        # Create a file in S3 bucket with the message as content
        bucket_name = os.getenv('buck_lm')
        file_name = f"{current_date}_SAT-ec2pubcheck.txt"
        s3.put_object(
            Body=f"{current_time} {message}",
            Bucket=bucket_name,
            Key=file_name
        )
        
    return {
        "statusCode": 200,
        "body": {
            "message": "Messages transferred to S3 successfully"
        }
    }
