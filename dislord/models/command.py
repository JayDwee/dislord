from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from models.base import BaseModel
from models.locale import Locale
from models.type import Snowflake


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


@dataclass
class ApplicationCommandOptionChoice(BaseModel):
    name: str
    value: [str, int, float]
    name_localizations: Optional[dict[Locale, str]] = None


@dataclass
class ApplicationCommandOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str

    name_localizations: Optional[dict[Locale, str]] = None
    description_localizations: Optional[dict[Locale, str]] = None
    required: Optional[bool] = None
    choices: Optional[list[ApplicationCommandOptionChoice]] = None
    options: Optional[list['ApplicationCommandOption']] = None
    # channel_types: Optional[list[ChannelType]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    autocomplete: Optional[bool] = None

# _ApplicationCommandOption = Union[ApplicationCommandOption]

class ApplicationCommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


@dataclass
class ApplicationCommand(BaseModel):
    id: Snowflake
    application_id: Snowflake
    guild_id: Snowflake
    name: str
    description: str
    version: Snowflake

    type: Optional[ApplicationCommandType] = None
    name_localizations: Optional[dict[Locale, str]] = None
    description_localizations: Optional[dict[Locale, str]] = None
    options: Optional[list[ApplicationCommandOption]] = None
    default_member_permissions: Optional[str] = None
    dm_permission: Optional[bool] = None
    default_permission: Optional[bool] = None
    nsfw: Optional[bool] = None
