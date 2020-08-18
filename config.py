# -*- coding: utf-8 -*-

from enum import Enum
import os


token = "1018507585:AAE34rim4NjeLn06e6N8C8xCCb3s_uQbziE"  # Telegram bot token
log_path = "LogFull.txt"  # all actions & success (bool): sign in, save game, load game, make a DB request
known_users_path = "KnownUsers.txt"  # username -> db_id
telegram_uids_path = "TelegramUsers.txt"  # telegram_uid -> username
user_db_path = "UsersDatabase.vdb"  # UserState -> JSON -> Vedis DB
ADMIN_NAME = "$ADMIN$"
HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 5000)


class State(Enum):
    START = 0
    INPUT_NAME = 1
    CHOOSE_LANG = 2
    HANDLE_FORK = 3
    SECRET_HANDLE_FORK = 42


class Lang(Enum):
    RUS = 0
    ENG = 1


class Action(Enum):
    INIT_KNOWN_USERS_DB_ID = 0
    ADD_USER_DB_ID = 1
    GET_USER_DB_ID = 2
    DUMP_KNOWN_USERS_DB_ID = 3
    LOAD_KNOWN_USERS_DB_ID = 4

    INIT_TELEGRAM_UIDS = 5
    ADD_USER_TELEGRAM_UID = 6
    GET_USERNAME_FROM_TELEGRAM_UID = 7
    DUMP_TELEGRAM_UIDS = 8
    LOAD_TELEGRAM_UIDS = 9

    SAVE_USER_IN_DB = 10
    LOAD_USER_FROM_DB = 11

    INIT_DATABASE_SELECTOR = 12
    SELECT_USERS_WITH_ACH_DONE = 13
    SELECT_USERS_WITH_LVL_DONE = 14
    SORT_USERS_BY_ACH_NUM = 15
    SORT_USERS_BY_LVL_NUM = 16

    SENT_STRANGE_CONTENT = 17
    ADD_NEW_TELEGRAM_UID = 18

    TELEGRAM_COMMAND_START = 19
    TELEGRAM_COMMAND_HELP = 20
    TELEGRAM_COMMAND_EXIT = 21
    TELEGRAM_COMMAND_INFO = 22
    TELEGRAM_TALKING = 23

    TELEGRAM_FIRST_ENTER = 24
    TELEGRAM_INPUT_NAME = 25
    TELEGRAM_CHOOSE_LANG = 26
    TELEGRAM_SECRETS_UNLOCKED = 27
    TELEGRAM_OFFENSIVE = 28
    TELEGRAM_QUESTION = 29
    TELEGRAM_THANKS = 30
    TELEGRAM_GREETING = 31
    TELEGRAM_BYE = 32
    TELEGRAM_LEVEL_17 = 33
    TELEGRAM_KEY_PHRASE = 34
    TELEGRAM_TRASH = 35

    SERVER_PING = 36
    SERVER_TIME = 37
    SERVER_SIGN_IN = 38
    SERVER_CREATE_USER = 39
    SERVER_SAVE_GAME = 40
    SERVER_LOAD_GAME = 41

