from discord_webhook import DiscordWebhook, DiscordEmbed
import traceback

def lambda_handler(event, context):

    try:
        # Get the new messages from the SQS Queue
        records = event['Records']

        for record in records:
            message = record['body'] # Assume record['body'] is a string, not a dictionary

            try:
                # Sends the Public EC2 Alert Notification!
                # if "Alert" in message and message['Alert'] == "Public_EC2_Instance":
                # Create a DiscordWebhook object with the URL of the Discord webhook
                webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")

                # Create a DiscordEmbed object to define the content of the message
                discord_message = f"Instance ID: {message['ID']}\nPublic IP: {message['Public_IP']}\nAttachment Time: {message['Time_Created']}"
                embed = DiscordEmbed(
                    title="Public EC2 Instance!",
                    description=discord_message,
                    color=0x03b2f8 # Use an integer value for color
                )
                webhook.add_embed(embed)
                webhook.execute() # Move this line inside the try block

                # Raises an error message and traceback if an error in receiving the messages occurs
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
