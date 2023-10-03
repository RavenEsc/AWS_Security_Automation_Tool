import logging
import os
import datetime
import boto3
import traceback
import json

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Get the new messages from the SQS Queue
        records = event.get('Records', [])  # Use get() to prevent KeyError

        # Create S3 client
        s3 = boto3.client('s3')  # Move outside the loop for efficiency
        
        for record in records:
            message = record['body']
            alertmessage = json.loads(record['body'])

            # Create time variables (current_time and current_date)
            current_time = datetime.datetime.now()
            current_date = datetime.date.today()
            print(list(alertmessage))
            
            counter = 1  # Initialize counter variable
            
            for alerts in alertmessage:
                alert = alerts['Alert']
                print(alert)
                try:
                    # Create a file in S3 bucket with the message as content
                    bucket_name = os.getenv('buck_lm')
                    folder_path = f"{current_date}/"
                    file_name = f"{folder_path}{current_time.strftime('%H:%M:%S')}-{alert}-{counter}.json"
                    
                    s3.put_object(
                        Body=message,
                        Bucket=bucket_name,
                        Key=file_name
                    )
                    
                    counter += 1  # Increment counter variable for each iteration
    
                # Handles the errors for creating the output log file in the S3 bucket
                except Exception as e:
                    traceback_message = traceback.format_exc()
                    logger.error(f"Error creating file in S3 bucket: {e}")
                    logger.error(traceback_message)
                    logger.error(message)
                    return {
                        "statusCode": 500,
                        "body": {"message": f"Error creating file in S3 bucket: {e}"}
                    }
                    
                    
    # Handles the errors for receiving the messages
    except Exception as e:
        traceback_message = traceback.format_exc()
        logger.error(f"Error receiving SQS message(s): {e}")
        logger.error(traceback_message)
        logger.error(message)
        return {
            "statusCode": 500,
            "body": {"message": f"Error receiving SQS message(s): {e}"}
        }

    # Code Ends, notifies code worked properly
    return {
        "statusCode": 200,
        "body": {"message": "Messages transferred to S3 successfully"}
    }
