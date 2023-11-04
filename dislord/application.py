import json

import requests
from discord_interactions import verify_key

from api import DiscordApi
from models.guild import Guild, PartialGuild
from .error import StateConfigurationException, DiscordApiException
from models.api import HttpResponse, HttpUnauthorized, HttpOk
from .models.interaction import Interaction, InteractionResponse, InteractionType


class ApplicationClient:
    def __init__(self, public_key, bot_token):
        self.commands = {}
        self.public_key = public_key
        self.api = DiscordApi(bot_token)

    def interact(self, raw_request, signature, timestamp) -> HttpResponse:
        if signature is None or timestamp is None or not verify_key(json.dumps(raw_request, separators=(',', ':'))
                                                                        .encode('utf-8'), signature, timestamp,
                                                                    self.public_key):
            return HttpUnauthorized('Bad request signature')
        req = Interaction.from_dict(raw_request)
        if req.type == InteractionType.PING:  # PING
            response_data = InteractionResponse.pong()  # PONG
        elif req.type == InteractionType.APPLICATION_COMMAND:
            data = req.data
            command_name = data.name
            response_data = self.commands[command_name](req)

        else:
            raise DiscordApiException(DiscordApiException.UNKNOWN_INTERACTION_TYPE.format(req.type))

        return HttpOk(response_data, headers={"Content-Type": "application/json"})

    def add_command(self, name, func):
        self.commands[name] = func

    def command(self, *, name):
        def decorator(func):
            self.add_command(name, func)
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

    def get_guilds(self):
        return self.api.get("/users/@me/guilds", type_hint=list[PartialGuild])
