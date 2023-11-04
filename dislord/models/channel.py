from dataclasses import dataclass
from enum import Enum
from typing import Optional

from models.base import BaseModel
from models.type import Snowflake
from models.user import User


class OverwriteType(Enum):
    ROLE = 0
    MEMBER = 1


@dataclass
class Overwrite(BaseModel):
    id: Snowflake
    type: OverwriteType
    allow: str
    deny: str


@dataclass
class Channel(BaseModel):
    id: Snowflake
    type: int
    guild_id: Optional[Snowflake]
    position: Optional[int]
    permission_overwrites: Optional[list[Overwrite]]
    name: Optional[str]
    topic: Optional[str]
    nsfw: Optional[bool]
    last_message_id: Optional[Snowflake]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[list[User]]
    icon: Optional[str]
    owner_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    managed: Optional[bool]
    parent_id: Optional[Snowflake]
    last_pin_timestamp: Optional[str]  # ISO8601 timestamp
    rtc_region: Optional[str]
    video_quality_mode: Optional[int]
    message_count: Optional[int]
    member_count: Optional[int]
    # thread_metadata: Optional[ThreadMetadata] FIXME
    # member: Optional[ThreadMember] FIXME
    default_auto_archive_duration: Optional[int]
    permissions: Optional[str]
    flags: Optional[int]
    total_message_sent: Optional[int]
    # available_tags: Optional[list[Tag]] FIXME
    applied_tags: Optional[list[Snowflake]]
    # default_reaction_emoji: Optional[DefaultReaction] FIXME
    default_thread_rate_limit_per_user: Optional[int]
    default_sort_order: Optional[int]
    default_forum_layout: Optional[int]