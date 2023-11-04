import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = dislord.ApplicationClient(PUBLIC_KEY, BOT_TOKEN)


@client.command(name="hello")
def hello(interaction: Interaction):
    guilds = client.get_guilds()
    return InteractionResponse.message(content="Servers:\n"+"\n".join([g.name for g in guilds]))


def serverless_handler(event, context):  # Not needed if using server
    client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
