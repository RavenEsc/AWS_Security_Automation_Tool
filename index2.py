import os
import datetime
import boto3
import traceback

def lambda_handler(event, context):
    try:
        # Get the new messages from the SQS Queue
        records = event['Records']
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error processing SQS messages: {e}","traceback": traceback_message}
        }

    for record in records:
        message = record['body']
        
        # Create S3 client
        s3 = boto3.client('s3')

        # Create time variables
        current_time = datetime.datetime.now()
        current_date = datetime.date.today()
    try:
        # Create a file in S3 bucket with the message as content
        bucket_name = os.getenv('buck_lm')
        folder_path = f"{current_date}/"
        file_name = f"{folder_path}{current_time.strftime('%H:%M:%S')}-ec2pubcheck.json"
        s3.put_object(
            Body=message,
            Bucket=bucket_name,
            Key=file_name
        )
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error creating file in S3 bucket: {e}", "traceback": traceback_message}
        }
    
    return {
        "statusCode": 200,
        "body": {"message": "Messages transferred to S3 successfully"}
    }
