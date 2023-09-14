import discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
import traceback

def lambda_handler(event, context):

    try:
        # Get the new messages from the SQS Queue
        records = event['Records']

        for record in records:
            message = record['body']

            try:
                # Sends the Public EC2 Alert Notification!
                if message['Alert'] == "Public_EC2_Instance":
                    # Create a DiscordWebhook object with the URL of the Discord webhook
                    webhook = discord_webhook.DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")

                    # Create a DiscordEmbed object to define the content of the message
                    discord_message = f"Instance ID: {message['ID']}\nPublic IP: {message['Alert']['Public_IP']}\nAttachment Time: {message['Alert']['Time_Created']}"
                    embed = discord_webhook.DiscordEmbed(
                        title="Public EC2 Instance!",
                        description=f"{discord_message}\n{message}\n:)",
                        color="03b2f8"
                    )
                    webhook.add_embed(embed)
                    webhook.execute()

                # Raises an error message and traceback if an error in recieving the messages occurs
            except Exception as e:
                traceback_message = traceback.format_exc()
                return {
                    "statusCode": 500,
                    "body": {"message": f"Error sending Discord message: {e}","traceback": traceback_message, "json_message": message}
                }
        # Raises an error message and traceback if an error in SENDING the messages occurs
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error processing SQS messages: {e}","traceback": traceback_message, "json_message": message}
        }

    return {
        "statusCode": 200,
        "body": {"message": "Discord Message Sent"}
    }
