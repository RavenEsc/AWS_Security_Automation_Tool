import logging
import os
import json
import boto3
import traceback
import socket

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Get the list of EC2 instances
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()

        # Check if the instances are public
        public_instances = []

        for instance in instances['Reservations']:
            for i in instance['Instances']:
                if 'PublicIpAddress' in i and i['PublicIpAddress']:
                    ip_address = i['PublicIpAddress']
                    open_ports = []

                    for port in range(0, 1025):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(.2)  # Sets timeout for the connection attempt
                        result = sock.connect_ex((ip_address, port))
                        if result == 0:
                            print(port)
                            open_ports.append(port)
                        sock.close()

                    if open_ports:
                        i['OpenPorts'] = open_ports
                        public_instances.append(i)
                elif 'PublicDnsName' in i and i['PublicDnsName']:
                    ip_address = i['PublicIpAddress']
                    open_ports = []

                    for port in range(0, 1025):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(.25)  # Set a timeout for the connection attempt
                        result = sock.connect_ex((ip_address, port))
                        if result == 0:
                            print(port)
                            open_ports.append(port)
                        sock.close()

                    if open_ports:
                        i['OpenPorts'] = open_ports
                        public_instances.append(i)
                    public_instances.append(i)

    # Handles the errors for reading the EC2 instances
    except Exception as e:
        traceback_msg = traceback.format_exc()
        logging.error(f"Error reading/listing EC2 instances: {str(e)}")
        logging.error(traceback_msg)
        return {
            'statusCode': 500,
            'body': {
                'message': f"Error reading/listing EC2 instances: {str(e)}"
            }
        }

    # Check if the public_instances list is empty
    if not public_instances:
        # Return a status code 200 with a body 'No Results to publish'
        return {
            'statusCode': 200,
            'body': 'No Results to publish'
        }
    else:
        # Filter to only instance-id
        filtered_instances = []
        for public_instance in public_instances:
            for network_interface in public_instance['NetworkInterfaces']:
                open_ports = public_instance['OpenPorts']
                instance = {
                    "Alert": "EC2_Public_Instance",
                    "ID": public_instance['InstanceId'],
                    "Public_IP": network_interface['Association']['PublicIp'],
                    "Time_Created": network_interface['Attachment']['AttachTime'],
                    "Open_Ports": list(open_ports)
                }
                filtered_instances.append(instance)

        # Publish the results to the SNS topic
        sns = boto3.client('sns')
        try:
            pub_message = json.dumps(filtered_instances, default=str, indent=4)
            sns.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=pub_message,
                Subject='List of Public EC2 Instances'
            )

            # Return a status code 200 with a body 'Results published to SNS'
            return {
                'statusCode': 200,
                'body': 'Results published to SNS'
            }

        # Handles the errors for pushing the results to the SNS topic
        except Exception as e:
            traceback_msg = traceback.format_exc()
            logging.error(f"Error publishing to SNS Topic: {str(e)}")
            logging.error(traceback_msg)
            logging.error(pub_message)
            return {
                'statusCode': 500,
                'body': {
                    'message': f"Error publishing to SNS Topic: {str(e)}"
                }
            }
