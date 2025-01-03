from enum import Enum

class UserEventEnum(str, Enum):
    CLICK_TABLE = "click_table"
    CLICK_LB = "click_lb"
    CLICK_WEEKLY_LB = "click_weekly_lb"
    CLICK_PLAY_NOW = "click_play_now"
    CLICK_JOIN = "click_join"
    CLICK_CREATE_TABLE = "click_create_table"
    CLICK_ADD_TO_SERVER = "click_add_to_server"
    CLICK_INVITE_OPEN_SEAT = "click_invite_open_seat"
    CLICK_INVITE_TOP_LEFT = "click_invite_top_left"
    CLICK_INVITE_LOWER_LEFT = "click_invite_lower_left"
    CLICK_JOIN_DISCORD_TABLE = "click_join_discord_table"
    CLICK_JOIN_DISCORD_LOBBY = "click_join_discord_lobby"
