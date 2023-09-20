import logging
import os
import json
import boto3
import traceback

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        policy_arn = 'arn:aws:iam::aws:policy/AdministratorAccess'

        # Get the list of all users attached to the policy
        iam = boto3.client('iam')
        policies = iam.list_entities_for_policy(PolicyArn=policy_arn)

        # Read the authorized IDs from the configuration file
        with open('authorized_ids.json') as f:
            authorized_ids = json.load(f)

        # Extract the authorized IDs for groups, users, and roles
        id_authorized_groups = authorized_ids['AuthorizedGroups']
        id_authorized_users = authorized_ids['AuthorizedUsers']
        id_authorized_roles = authorized_ids['AuthorizedRoles']

        # Check if the policy is used where it shouldn't be
        Unauthorized_Admins = []

        for group in policies['PolicyGroups']:
            group_id = group['GroupId']
            if group_id not in id_authorized_groups:
                Unauthorized_Admins.append(group)

        for user in policies['PolicyUsers']:
            user_id = user['UserId']
            if user_id not in id_authorized_users:
                Unauthorized_Admins.append(user)

        for role in policies['PolicyRoles']:
            Role_id = role['RoleId']
            if Role_id not in id_authorized_roles:
                Unauthorized_Admins.append(role)
    
    # Handles the errors for reading the IAM entities by policy
    except Exception as e:
        traceback_msg = traceback.format_exc()
        logging.error(f"Error reading/listing IAM Entities: {str(e)}")
        logging.error(traceback_msg)
        return {
                'statusCode': 500,
                'body': {"message": f"Error reading/listing IAM Entities: {str(e)}"}
            }

    # Check if the Unauthorized_Admins list is empty
    if not Unauthorized_Admins:
        # Return a status code 200 with a body 'No Results to publish'
        return {'statusCode': 200, 'body': 'No Results to publish'}
    else:
        # Filter to only UserName and UserID
        filtered_UnAuth = []
        for Unauthorized_Admin in Unauthorized_Admins:
            if 'UserName' in Unauthorized_Admin:
                Group = {
                        "Alert": "Unauthorized_Admin_Group",
                        "Group": Unauthorized_Admin['GroupName'],
                        "ID": Unauthorized_Admin['GroupId'],
                    }
                filtered_UnAuth.append(Group)

            elif 'UserName' in Unauthorized_Admin:
                User = {
                        "Alert": "Unauthorized_Admin_User",
                        "User": Unauthorized_Admin['UserName'],
                        "ID": Unauthorized_Admin['UserId'],
                    }
                filtered_UnAuth.append(User)

            elif 'RoleName' in Unauthorized_Admin:
                Role = {
                        "Alert": "Unauthorized_Admin_Role",
                        "Role": Unauthorized_Admin['RoleName'],
                        "ID": Unauthorized_Admin['RoleId'],
                    }
                filtered_UnAuth.append(Role)


        # Publish the results to the SNS topic
        sns = boto3.client('sns')
        try:
            pub_message=json.dumps(filtered_UnAuth, default=str, indent=4)
            sns.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=pub_message,
                Subject='List of Unauthorized_Admins'
            )

            # Return a status code 200 with a body 'Results published to SNS'
            return {'statusCode': 200, 'body': 'Results published to SNS'}
        
        # Handles the errors for pushing the results to the SNS topic
        except Exception as e:
            traceback_msg = traceback.format_exc()
            logging.error(f"Error publishing to SNS Topic: {str(e)}")
            logging.error(traceback_msg)
            logging.error(pub_message)
            return {
                'statusCode': 500,
                'body': {"message": f"Error publishing to SNS Topic: {str(e)}"}
                }
