import json
import requests

from error import DiscordApiException
from models.base import cast

DISCORD_API_VERSION = 10
DISCORD_URL = f"https://discord.com/api/v{DISCORD_API_VERSION}"
# WARNING: Average time to call and get response from API is 25ms, not great to call lots if you want quick processing


class DiscordApi:
    def __init__(self, client, bot_token):
        self.client = client
        self.bot_token = bot_token
        self.auth_header = {"Authorization": "Bot " + self.bot_token}

    def get(self, url, params=None, type_hint=None, **kwargs):
        response = requests.get(DISCORD_URL+url, params, **kwargs, headers=self.auth_header)
        if response.ok:
            return cast(json.loads(response.content), type_hint, client=self.client)
        else:
            raise DiscordApiException(f"{response.status_code} {response.text} error when calling discord API URL: {url} Params: {params}")
