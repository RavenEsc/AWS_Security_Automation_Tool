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
                id = item['ID']
                public_ip = item['Public_IP']
                time_created = item['Time_Created']
                
                try:
                    # Sends the message formatted to be easily readable to Discord channel webhook integration
                    webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")
                    embed = DiscordEmbed(
                        title="Public EC2 Instance!",
                        description=f"Instance ID: {id}\nPublic IP: {public_ip}\nAttachment Time: {time_created}",
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
