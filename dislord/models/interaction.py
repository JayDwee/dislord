from dataclasses import dataclass
from typing import Optional
from enum import Enum

from dislord.models.base import BaseModel
from dislord.models.type import Snowflake


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


@dataclass
class InteractionData(BaseModel):
    id: Snowflake
    name: str
    type: int
    # resolved: Optional[ResolvedData] FIXME
    # options: Optional[list[ApplicationCommandInteractionDataOption]] FIXME
    guild_id: Optional[Snowflake]
    target_id: Optional[Snowflake]


@dataclass
class Interaction(BaseModel):
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    token: str
    version: int
    # entitelements: list[Entitlement] FIXME

    data: Optional[InteractionData]
    guild_id: Optional[Snowflake]
    # channel: Optional[PartialChannel] FIXME
    channel_id: Optional[Snowflake]
    # member: Optional[GuildMember] FIXME
    # user: Optional[User] FIXME
    # message: Optional[Message] FIXME
    app_permissions:  Optional[str]
    locale:  Optional[str]  # This is available on all interaction types except PING
    guild_locale: Optional[str]


class InteractionCallbackType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7  # Only valid for component-based interactions
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9  # Not available for MODAL_SUBMIT and PING interactions.
    PREMIUM_REQUIRED = 10  # Not available for APPLICATION_COMMAND_AUTOCOMPLETE and PING interactions.


@dataclass
class InteractionCallbackData(BaseModel):
    flags: Optional[int]
    # components: list[Component] FIXME
    # attachments: list[PartialAttachment] FIXME

    tts: Optional[bool]
    content: Optional[str]
    # embeds: Optional[list[Embed]] FIXME
    # allowed_mentions: Optional[AllowedMentions] FIXME


@dataclass
class InteractionResponse(BaseModel):
    type: InteractionCallbackType
    data: Optional[InteractionCallbackData] = None

    @staticmethod
    def pong():
        return InteractionResponse(InteractionCallbackType.PONG)

    @staticmethod
    def message(**kwargs):
        cls = InteractionResponse(InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                                  InteractionCallbackData.from_dict(kwargs))
        return cls
