import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

client = dislord.ApplicationClient(DISCORD_PUBLIC_KEY)


@client.command(name="hello")
def hello(interaction: Interaction):
    return InteractionResponse.message(content="hello world " + interaction.id)


def serverless_handler(event, context):  # Not needed if using server
    client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
