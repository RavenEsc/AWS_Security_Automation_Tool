import os
import json
import boto3

def lambda_handler(event, context):
    # Get the list of EC2 instances
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()

    # Check if the instances are public
    public_instances = []
    for instance in instances['Reservations']:
        for i in instance['Instances']:
            if i['PublicDnsName'] is not None:
                public_instances.append(i)

    # Publish the results to the SNS topic
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.getenv('SNS_TOPIC_ARN'),
        Message=json.dumps(public_instances),
        Subject='List of Public EC2 Instances'
    )

    # Return a success message
    return {'statusCode': 200, 'body': 'Results published to SNS'}
