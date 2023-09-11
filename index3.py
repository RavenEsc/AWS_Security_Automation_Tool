import requests
import traceback

def lambda_handler(event, context):

    try:
        # Get the new messages from the SQS Queue
        message = event.get("Message")
    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error processing SQS messages: {e}", "traceback": traceback_message}
        }

    try:
        # Create a payload dictionary with the content of the message
        payload = {
            "content": f"Alert!\n{message} :)",
            "username": "Webhook Bot",
            "embeds": []
        }

        # Send a POST request to the Discord webhook URL
        response = requests.post("https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy", json=payload)

        # Check the response status code
        if response.status_code != 204:
            raise Exception(f"Failed to send Discord message. Response: {response.text}")

    except Exception as e:
        traceback_message = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": {"message": f"Error sending Discord message: {e}", "traceback": traceback_message}
        }

    return {
        "statusCode": 200,
        "body": {"message": "Discord Message Sent"}
    }
