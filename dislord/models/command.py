from dataclasses import dataclass, MISSING
from enum import Enum
from typing import Optional, Union

from models.base import BaseModel
from models.locale import Locale
from models.type import Snowflake, PartialOptional


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
    id: PartialOptional[Snowflake]
    application_id: PartialOptional[Snowflake]
    guild_id: Optional[Snowflake]
    name: str
    description: Optional[str]
    version: PartialOptional[Snowflake]

    type: Optional[ApplicationCommandType]
    name_localizations: Optional[dict[Locale, str]]
    description_localizations: Optional[dict[Locale, str]]
    options: Optional[list[ApplicationCommandOption]]
    default_member_permissions: Optional[str]
    dm_permission: Optional[bool]
    default_permission: Optional[bool]
    nsfw: Optional[bool]

    def __eq__(self, other):
        eq_list = ['guild_id', 'name', 'description', 'type', 'name_localization', 'description_localizations',
                   'options', 'default_member_permissions', 'dm_permission', 'default_permission', 'nsfw']
        result = True
        for eq_attr in eq_list:
            self_attr = getattr(self, eq_attr, None)
            other_attr = getattr(other, eq_attr, None)
            result = result and (self_attr if self_attr is not MISSING else None) \
                == (other_attr if other_attr is not MISSING else None)
        return result
