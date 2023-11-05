import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = dislord.ApplicationClient(PUBLIC_KEY, BOT_TOKEN)


@client.command(name="simple", description="Simple Command", guild_ids=['590643624358969350', '748515497913483416'])
def simple(interaction: Interaction):
    guilds = client.guilds
    return InteractionResponse.message(content="Servers:\n"+"\n".join([f"{g.name} {g.afk_timeout}" for g in guilds]))


def serverless_handler(event, context):  # Not needed if using server
    return client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    client.sync_commands()
    client.sync_commands(guild_ids=[g.id for g in client.guilds])
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
