from typing import Optional
from dataclasses import dataclass

from models.base import BaseModel
from models.type import Snowflake


@dataclass
class PartialGuild(BaseModel):
    id: Snowflake
    name: str
    # features: list[GuildFeature] FIXME: Add Enum
    icon: Optional[str]
    owner: Optional[bool]
    permissions: Optional[str]
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]


@dataclass
class Guild(PartialGuild):
    owner_id: Snowflake
    afk_timeout: int
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    # roles: list[Role] FIXME: Add Enum
    # emojis: list[Emoji] FIXME: Add Enum
    mfa_level: int
    system_channel_flags: int
    premium_tier: int
    public_updates_channel_id: Snowflake
    nsfw_level: int
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: Optional[Snowflake]
    icon_hash: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    region: Optional[str]
    afk_channel_id: Optional[Snowflake]
    widget_enabled: Optional[bool]
    widget_channel_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    rules_channel_id: Optional[Snowflake]
    max_presences: Optional[int]
    max_members: Optional[int]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    preferred_locale: Optional[str]
    max_video_channel_users: Optional[int]
    # welcome_screen: Optional[WelcomeScreen] FIXME
    # stickers: Optional[list[Sticker]] FIXME
