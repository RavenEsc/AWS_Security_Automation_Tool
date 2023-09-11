from discord_webhook import DiscordWebhook, DsicordEmbed
import traceback

def lambda_handler(event, context):

    try:
        # Get the new messages from the SQS Queue
        message = event.get("Message")
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error processing SQS messages: {e}","traceback": traceback_message}
        }

    try:
        # Create a DiscordWebhook object with the URL of the Discord webhook
        webhook = discord_webhook.DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")

        # Create a DiscordEmbed object to define the content of the message
        embed = discord_webhook.DiscordEmbed(
            title="Alert!",
            description=f"{message} :)",
            color="03b2f8"
        )
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error sending Discord message: {e}","traceback": traceback_message}
        }

    return {
        "statusCode": 200,
        "body": {"message": "Discord Message Sent"}
    }
