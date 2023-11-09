import os

import dislord
from dislord.models.interaction import Interaction, InteractionResponse
from dislord import CommandGroup

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

client = dislord.ApplicationClient(PUBLIC_KEY, BOT_TOKEN)


command_group = CommandGroup(name="group", description="Command Group")


@command_group.command(name="groupcommand", description="Group Command")
def group_command(interaction: Interaction):
    return InteractionResponse.message(content="Group Command Response")


# sub_command_group = CommandGroup(name="subgroup", description="Sub Command Group", parent=command_group)
#
#
# @sub_command_group.command(name="subgroupcommand", description="Sub Group Command")
# def sub_group_command(interaction: Interaction):
#     return InteractionResponse.message(content="Sub Group Command Response")


def serverless_handler(event, context):  # Not needed if using server
    client.register_group(command_group)
    client.sync_commands()
    # client.register_group(sub_command_group)
    return client.serverless_handler(event, context)


if __name__ == '__main__':  # Not needed if using serverless
    client.register_group(command_group)
    client.sync_commands()
    # client.register_group(sub_command_group)
    dislord.server.start_server(client, host='0.0.0.0', debug=True, port=8123)
