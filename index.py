import os
import json
import boto3
import traceback

def lambda_handler(event, context):
    try: # Get the list of EC2 instances
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()

        # Check if the instances are public
        public_instances = []
        for instance in instances['Reservations']:
            for i in instance['Instances']:
                if i['NetworkInterfaces'][0]['PublicIpv4Address'] is not None:
                    public_instances.append(i)
                elif i['PublicDnsName'] is not None:
                    public_instances.append(i)

    except Exception as e:
        traceback_msg = traceback.format_exc()
        return {'statusCode': str(e.response['ResponseMetadata']['HTTPStatusCode']), 'body': str(e), 'traceback': traceback_msg}
        # Code ends here if there is an error

    # Check if the public_instances list is empty
    if not public_instances:
        # Return a status code 200 with a body 'No Results to publish'
        return {'statusCode': 200, 'body': 'No Results to publish'}
    else:
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
        except Exception as s:
            traceback_msg = traceback.format_exc()
            return {'statusCode': str(s.response['ResponseMetadata']['HTTPStatusCode']), 'body': str(s), 'traceback': traceback_msg}