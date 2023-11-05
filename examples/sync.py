import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_GUILD_ID = os.environ.get("OWNER_GUILD_ID")

client = dislord.ApplicationClient(PUBLIC_KEY, BOT_TOKEN)


@client.command(name="hello", description="Hello World!")
def hello(interaction: Interaction):
    return InteractionResponse.message(content=f"Hello {interaction.user.username}")


@client.command(name="sync", description="Sync Command", guild_ids=[OWNER_GUILD_ID])
def hello(interaction: Interaction):
    client.sync_commands()
    client.sync_commands(guild_ids=[g.id for g in client.guilds])
    return InteractionResponse.message(content="Sync Complete")


def serverless_handler(event, context):  # Not needed if using server
    client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    client.sync_commands()
    client.sync_commands(guild_ids=[g.id for g in client.guilds])
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
