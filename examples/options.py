import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse
from models.command import ApplicationCommandOption, ApplicationCommandOptionType

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = dislord.ApplicationClient(PUBLIC_KEY, BOT_TOKEN)


@client.command(name="add", description="Add together numbers",
                options=[ApplicationCommandOption.from_kwargs(name="a", description="First integer to add",
                                                              type=ApplicationCommandOptionType.INTEGER, client=client),
                         ApplicationCommandOption.from_kwargs(name="b", description="Second integer to add",
                                                              type=ApplicationCommandOptionType.INTEGER, client=client)
                         ]
                )
def add(interaction: Interaction, a: int, b: int):
    return InteractionResponse.message(content=f"{a} + {b} = {a+b}")


def serverless_handler(event, context):  # Not needed if using server
    client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    client.sync_commands()
    client.sync_commands(guild_ids=[g.id for g in client.guilds])
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
