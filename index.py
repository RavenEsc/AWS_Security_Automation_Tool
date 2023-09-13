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
                if 'NetworkInterfaces' in i and i['NetworkInterfaces'][0].get('PublicIpv4Address'):
                    public_instances.append(i)
                elif 'PublicDnsName' in i and i['PublicDnsName']:
                    public_instances.append(i)

    except Exception as e:
        traceback_msg = traceback.format_exc()
        return {'statusCode': 500,
                'body': {"message": f"Error reading/listing EC2 instances: {str(e)}", 'traceback': traceback_msg}
                }
        # Code ends here if there is an error

    # Check if the public_instances list is empty
    if not public_instances:
        # Return a status code 200 with a body 'No Results to publish'
        return {'statusCode': 200, 'body': 'No Results to publish'}
    else:
        # Filter to only instance-id
        filtered_instances = []
        for public_instance in public_instances:
            for network_interface in public_instance['NetworkInterfaces']:
                filtered_instances.append(public_instance['InstanceId'])
                filtered_instances.append(network_interface['Association']['PublicIp'])
                filtered_instances.append(network_interface['Attachment']['AttachTime'])


        # Publish the results to the SNS topic
        sns = boto3.client('sns')
        try:
            pub_message=json.dumps(filtered_instances, default=str, indent=4)
            sns.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=pub_message,
                Subject='List of Public EC2 Instances'
            )

            # Return a status code 200 with a body 'Results published to SNS'
            return {'statusCode': 200, 'body': 'Results published to SNS'}
        except Exception as e:
            traceback_msg = traceback.format_exc()
            return {
                'statusCode': 500,
                'body': {"message": f"Error publishing to SNS Topic: {str(e)}", 'traceback': traceback_msg, 'json_message': pub_message}
                }
