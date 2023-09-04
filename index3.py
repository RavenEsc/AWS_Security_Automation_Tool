import discord_webhook

def lambda_handler(event, context):
    webhook = discord_webhook.DiscordWebhook(url="https://discordapp.com/api/webhooks/1147701063630196786/PVU9g477tn2u9ko0LZ5uTg4SUoQGqe_iSftGdhjZi1Szz5aIDDEew4soEPL80S3EYizy")

    embed = discord_webhook.DiscordEmbed(
        title="Taco Love",
        description="You deserve some taco love today!",
        color="03b2f8"
    )

    embed.set_image(url="https://cdn.dribbble.com/users/545781/screenshots/3157610/happy-taco.jpg")
    webhook.add_embed(embed)
    webhook.execute()

    return {
        "statusCode": 200,
        "body": {"message": "Hello World"}
    }
