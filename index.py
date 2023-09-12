import os
import json
import boto3
import traceback
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Get the current datetime
        current_datetime = datetime.now().isoformat()

        # Get the list of EC2 instances
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()

        # Check if the instances are public
        public_instances = []
        for instance in instances['Reservations']:
            for i in instance['Instances']:
                if 'NetworkInterfaces' in i and i['NetworkInterfaces'][0].get('PublicIpv4Address'):
                    public_instances.append(i)
                elif 'PublicDnsName' in i and i['PublicDnsName']:
                    public_instances.append(i)

    except Exception as e:
        traceback_msg = traceback.format_exc()
        return {
            'statusCode': 500,
            'body': {
                "message": f"Error reading/listing EC2 instances: {str(e)}",
                'traceback': traceback_msg
            }
        }

    # Check if the public_instances list is empty
    if not public_instances:
        # Return a status code 200 with a body 'No Results to publish'
        return {'statusCode': 200, 'body': 'No Results to publish'}
    else:
        # Add the current datetime to the public_instances list
        for instance in public_instances:
            instance['CurrentDatetime'] = current_datetime

        # Publish the results to the SNS topic
        sns = boto3.client('sns')
        try:
            sns.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=json.dumps(public_instances),
                Subject='List of Public EC2 Instances'
            )

            # Return a status code 200 with a body 'Results published to SNS'
            return {'statusCode': 200, 'body': 'Results published to SNS'}
        except Exception as e:
            traceback_msg = traceback.format_exc()
            return {
                'statusCode': 500,
                'body': {
                    "message": f"Error publishing to SNS Topic: {str(e)}",
                    'traceback': traceback_msg
                }
            }
