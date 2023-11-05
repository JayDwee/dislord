import json
from typing import Callable

import requests
from discord_interactions import verify_key

from api import DiscordApi
from models.application import Application
from models.channel import Channel
from models.command import ApplicationCommand, ApplicationCommandType
from models.guild import Guild, PartialGuild
from models.type import Snowflake
from models.user import User
from .error import StateConfigurationException, DiscordApiException
from models.api import HttpResponse, HttpUnauthorized, HttpOk
from .models.interaction import Interaction, InteractionResponse, InteractionType


class ApplicationClient:
    def __init__(self, public_key, bot_token):
        self.commands = {}
        self.command_callbacks = {}
        self.public_key = public_key
        self.api = DiscordApi(self, bot_token)

        self._application = None

    def interact(self, raw_request, signature, timestamp) -> HttpResponse:
        if signature is None or timestamp is None or not verify_key(json.dumps(raw_request, separators=(',', ':'))
                                                                        .encode('utf-8'), signature, timestamp,
                                                                    self.public_key):
            return HttpUnauthorized('Bad request signature')
        req = Interaction.from_dict(raw_request, self)
        if req.type == InteractionType.PING:  # PING
            response_data = InteractionResponse.pong()  # PONG
        elif req.type == InteractionType.APPLICATION_COMMAND:
            data = req.data
            command_name = data.name
            response_data = self.command_callbacks[command_name](req)

        else:
            raise DiscordApiException(DiscordApiException.UNKNOWN_INTERACTION_TYPE.format(req.type))

        return HttpOk(response_data, headers={"Content-Type": "application/json"})

    def add_command(self, command: ApplicationCommand, callback: Callable):
        self.command_callbacks[command.name] = callback
        self.commands[command.name] = command

    def command(self, *, name, description, dm_permission=True, nsfw=False):
        def decorator(func):
            self.add_command(ApplicationCommand.from_kwargs(name=name, description=description,
                                                            type=ApplicationCommandType.CHAT_INPUT,
                                                            dm_permission=dm_permission, nsfw=nsfw, client=self), func)
            return func

        return decorator

    def serverless_handler(self, event, context):
        if event['httpMethod'] == "POST":
            print(f"🫱 Full Event: {event}")
            raw_request = json.loads(event["body"])
            print(f"👉 Request: {raw_request}")
            raw_headers = event["headers"]
            signature = raw_headers.get('x-signature-ed25519')
            timestamp = raw_headers.get('x-signature-timestamp')
            response = self.interact(raw_request, signature, timestamp).as_serverless_response()
            print(f"🫴 Response: {response}")
            return response

    @property
    def application(self):
        if self._application is None:
            self._application = self.get_application()
        return self._application

    def get_application(self):
        return self.api.get("/applications/@me", type_hint=Application)

    def sync_commands(self, guild_id: Snowflake = None, application_id: Snowflake = None):
        registered_commands = self._get_commands(guild_id)
        missing_commands = list(self.commands.values())
        for registered_command in registered_commands:
            if registered_command not in self.commands.values():
                self._delete_commands(command_id=registered_command.id, guild_id=guild_id,
                                      application_id=registered_command.application_id)
            else:
                missing_commands.remove(registered_command)

        for missing_command in missing_commands:
            self._register_command(missing_command, guild_id=guild_id, application_id=application_id)

    def _get_commands(self, guild_id: Snowflake = None, application_id: Snowflake = None,
                      with_localizations: bool = None) -> list[ApplicationCommand]:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"

        params = {}
        if with_localizations is not None:
            params["with_localizations"] = with_localizations

        return self.api.get(f"{endpoint}/commands", params=params, type_hint=list[ApplicationCommand])

    def _delete_commands(self, command_id: Snowflake,
                         guild_id: Snowflake = None, application_id: Snowflake = None) -> None:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"

        self.api.delete(f"{endpoint}/commands/{command_id}")



    def _register_command(self, application_command: ApplicationCommand,
                         guild_id: Snowflake = None, application_id: Snowflake = None) -> ApplicationCommand:
        endpoint = f"/applications/{application_id if application_id else self.application.id}"
        if guild_id:
            endpoint += f"/guilds/{guild_id}"
        return self.api.post(f"{endpoint}/commands", application_command, type_hint=ApplicationCommand)

    def get_user(self, user_id=None) -> User:
        return self.api.get(f"/users/{user_id if user_id else '@me'}", type_hint=User)

    def get_guild(self, guild_id) -> Guild:
        return self.api.get(f"/guilds/{guild_id}", type_hint=Guild)

    def get_guilds(self) -> list[PartialGuild]:
        return self.api.get("/users/@me/guilds", type_hint=list[PartialGuild])

    def get_channel(self, channel_id) -> list[Channel]:
        return self.api.get(f"/channels/{channel_id}", type_hint=list[Channel])
