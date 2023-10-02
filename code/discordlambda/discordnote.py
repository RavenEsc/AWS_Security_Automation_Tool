import logging
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import traceback
# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    try:
        # Pulls from SQS event trigger, checks each result in the list, sets each necessary value within the elements read
        records = event['Records']
        for record in records:
            message = json.loads(record['body'])
            for item in message:
                # Alert Value so far between 'EC2_Public_Instance', 
                alert = item['Alert']
            # EC2 Public Instance
                if alert == 'EC2_Public_Instance':
                    # EC2 values set as variables
                    id = item['ID']
                    public_ip = item['Public_IP']
                    time_created = item['Time_Created']
                    
                    delim = ", "
                    open_ports = delim.join(map(str, item['Open_Ports']))

                    try:
                        # Sends the PublicEC2 Alert message formatted to be easily readable to Discord channel webhook integration, pings all users who can see the channel
                        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")
                        embed = DiscordEmbed(
                            title="Public EC2 Instance!",
                            description=f"Instance ID: {id}\nPublic IP: {public_ip}\nAttachment Time: {time_created}\nOpen Ports: {open_ports}\n\n@everyone",
                            allowed_mentions={"everyone"},
                            color=0x03b2f8
                        )
                        webhook.add_embed(embed)
                        webhook.execute()
                    # Handles the errors for sending the messages to Discord
                    except Exception as e:
                        traceback_message = traceback.format_exc()
                        logger.error(f"Error sending Discord message: {e}")
                        logger.error(traceback_message)
                        logger.error(message)
                        return {
                            "statusCode": 500,
                            "body": {"message": f"Error sending Discord message: {e}"}
                        }
                    
            # IAM Group Admin
                elif alert == 'Unauthorized_Admin_Group':
                    # IAM values set as variables
                    group = item['Group']
                    group_id = item['ID']

                    try:
                        # Sends the PublicEC2 Alert message formatted to be easily readable to Discord channel webhook integration, pings all users who can see the channel
                        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")
                        embed = DiscordEmbed(
                            title="Unauthorized Admin!",
                            description=f"Group Name: {group}\nID: {group_id}\n\n@everyone",
                            allowed_mentions={"everyone"},
                            color=0x03b2f8
                        )
                        webhook.add_embed(embed)
                        webhook.execute()
                    # Handles the errors for sending the messages to Discord
                    except Exception as e:
                        traceback_message = traceback.format_exc()
                        logger.error(f"Error sending Discord message: {e}")
                        logger.error(traceback_message)
                        logger.error(message)
                        return {
                            "statusCode": 500,
                            "body": {"message": f"Error sending Discord message: {e}"}
                    }
            # IAM Admin User
                elif alert == 'Unauthorized_Admin_User':
                    # IAM values set as variables
                    user = item['User']
                    user_id = item['ID']

                    try:
                        # Sends the PublicEC2 Alert message formatted to be easily readable to Discord channel webhook integration, pings all users who can see the channel
                        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")
                        embed = DiscordEmbed(
                            title="Unauthorized Admin!",
                            description=f"User Name: {user}\nID: {user_id}\n\n@everyone",
                            allowed_mentions={"everyone"},
                            color=0x03b2f8
                        )
                        webhook.add_embed(embed)
                        webhook.execute()
                    # Handles the errors for sending the messages to Discord
                    except Exception as e:
                        traceback_message = traceback.format_exc()
                        logger.error(f"Error sending Discord message: {e}")
                        logger.error(traceback_message)
                        logger.error(message)
                        return {
                            "statusCode": 500,
                            "body": {"message": f"Error sending Discord message: {e}"}
                    }
            # IAM Admin Role
                elif alert == 'Unauthorized_Admin_Role':
                    # IAM values set as variables
                    role = item['Role']
                    role_id = item['ID']

                    try:
                        # Sends the PublicEC2 Alert message formatted to be easily readable to Discord channel webhook integration, pings all users who can see the channel
                        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")
                        embed = DiscordEmbed(
                            title="Unauthorized Admin!",
                            description=f"Role Name: {role}\nID: {role_id}\n\n@everyone",
                            allowed_mentions={"everyone"},
                            color=0x03b2f8
                        )
                        webhook.add_embed(embed)
                        webhook.execute()
                    # Handles the errors for sending the messages to Discord
                    except Exception as e:
                        traceback_message = traceback.format_exc()
                        logger.error(f"Error sending Discord message: {e}")
                        logger.error(traceback_message)
                        logger.error(message)
                        return {
                            "statusCode": 500,
                            "body": {"message": f"Error sending Discord message: {e}"}
                    }
    # Handles the errors for recieving the messages to Discord
    except Exception as e:
        traceback_message = traceback.format_exc()
        logger.error(f"Error processing SQS messages: {e}")
        logger.error(traceback_message)
        logger.error(message)
        return {
            "statusCode": 500,
            "body": {"message": f"Error processing SQS messages: {e}"}
        }
    # Code Ends, notifies code worked properly
    return {
        "statusCode": 200,
        "body": {"message": "Discord message sent successfully"}
    }