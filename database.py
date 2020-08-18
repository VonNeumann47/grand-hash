# -*- coding: utf-8 -*-

from copy import deepcopy
import json
import os
from time import time
from vedis import Vedis
import yadisk

from config import State, Lang, Action, \
                   log_path, known_users_path, telegram_uids_path, user_db_path, \
                   ADMIN_NAME, OAUTH_TOKEN, YADISK_PATH


def cloud_download_files():
    need_to_download = []
    for path in [log_path,
                 known_users_path,
                 telegram_uids_path,
                 user_db_path,
                 'Swears.txt']:
        if not os.path.exists(path):
            need_to_download.append(path)
    if need_to_download:
        y = yadisk.YaDisk(token=OAUTH_TOKEN)
        if not y.check_token():
            raise ValueError("OAUTH_TOKEN expired :(")
        for path in need_to_download:
            y.download(f"{YADISK_PATH}/{path}", path)

def cloud_upload_files():
    y = yadisk.YaDisk(token=OAUTH_TOKEN)
    if not y.check_token():
        raise ValueError("OAUTH_TOKEN expired :(")
    if not y.exists(YADISK_PATH):
        y.mkdir(YADISK_PATH)
    for path in [log_path,
                 known_users_path,
                 telegram_uids_path,
                 user_db_path,
                 'Swears.txt']:
        yapath = f"{YADISK_PATH}/{path}"
        if y.exists(yapath):
            y.remove(yapath, permanently=True)
        y.upload(path, yapath)


class Logger:
    def __init__(self, init_file=False):
        self.path = log_path
        if init_file:
            with open(self.path, 'w', encoding='utf-8') as fout:
                print("Username".center(15),
                      "Action type".center(30),
                      "Success".center(10),
                      "Timestamp".center(15),
                      "Additional information".center(30),

                      sep='|',
                      file=fout)
                print("-" * 104, file=fout)

    def log(self, username, action, success, additional_info=""):
        timestamp = int(time())
        with open(self.path, 'a', encoding='utf-8') as fout:
            print(username.center(15),
                  action.name.center(30),
                  str(success).center(10),
                  str(timestamp).center(15),
                  additional_info.center(30),

                  sep='|',
                  file=fout)

cloud_download_files()
logger = Logger()


class UsernameToDBUid:
    def copy(self, other):
        self.path = other.path
        self.max_id = other.max_id
        self.map = deepcopy(other.map)
        
    def __init__(self, init_from_file=True, logging=True):
        self.path = known_users_path
        self.max_id = 0
        self.map = dict()
        if init_from_file:
            self.copy(UsernameToDBUid.load_from_file(logging))
        if logging:
            logger.log(ADMIN_NAME, Action.INIT_KNOWN_USERS_DB_ID, True, "INIT_FROM_FILE" if init_from_file else "")

    def user_exists(self, username, force_update=True):
        if force_update:
            self.copy(UsernameToDBUid.load_from_file(logging=False))
        return username in self.map.keys()

    def add_user(self, username, force_update=True, logging=True):
        try:
            if force_update:
                self.copy(UsernameToDBUid.load_from_file(logging=False))
            if username in self.map.keys():
                raise ValueError("User with this name already exists!")
            self.max_id += 1
            self.map[username] = self.max_id
            with open(self.path, 'a', encoding='utf-8') as fout:
                print(username, self.max_id, file=fout)
            with Vedis(user_db_path) as db:
                db[self.max_id] = UserState(username).toJSON()
            if logging:
                logger.log(username, Action.ADD_USER_DB_ID, True)
            return True
        except ValueError:
            if logging:
                logger.log(username, Action.ADD_USER_DB_ID, False, "USER_ALREADY_EXISTS")
            raise
        except:  # shouldn't cause any problems!
            if logging:
                logger.log(username, Action.ADD_USER_DB_ID, False, "UNKNOWN_PROBLEM")
            raise

    def get_id(self, username, force_update=True, logging=True):
        try:
            if force_update:
                self.copy(UsernameToDBUid.load_from_file(logging=False))
            uid = self.map[username]
            if logging:
                logger.log(username, Action.GET_USER_DB_ID, True, str(uid))
            return uid
        except KeyError:  # no such username yet
            if logging:
                logger.log(username, Action.GET_USER_DB_ID, False, "UNKNOWN_USERNAME")
            raise KeyError(f"User {username} was not found in UserStates DB")

    def dump_to_file(self, logging=True):
        with open(self.path, 'w', encoding='utf-8') as fout:
            for username, uid in self.map.items():
                print(username, uid, file=fout)
        if logging:
            logger.log(ADMIN_NAME, Action.DUMP_KNOWN_USERS_DB_ID, True)

    def load_from_file(logging=True):
        try:
            target = UsernameToDBUid(init_from_file=False, logging=False)
            with open(target.path, 'r', encoding='utf-8') as fin:
                for line in fin:
                    username, uid = line.strip().split()
                    uid = int(uid)
                    target.map[username] = uid
                    target.max_id = max(target.max_id, uid)
            if logging:
                logger.log(ADMIN_NAME, Action.LOAD_KNOWN_USERS_DB_ID, True)
            return target
        except:  # syntax error in file
            if logging:
                logger.log(ADMIN_NAME, Action.LOAD_KNOWN_USERS_DB_ID, False, "COULD_NOT_PARSE")
            raise IOError("Couldn't parse file as UsernameToDBUid")

username_to_db_id = UsernameToDBUid()


class TelegramToUsername:
    def copy(self, other):
        self.path = other.path
        self.map = deepcopy(other.map)
        
    def __init__(self, init_from_file=True, logging=True):
        self.path = telegram_uids_path
        self.map = dict()
        if init_from_file:
            self.copy(TelegramToUsername.load_from_file(logging))
        if logging:
            logger.log(ADMIN_NAME, Action.INIT_TELEGRAM_UIDS, True, "INIT_FROM_FILE" if init_from_file else "")

    def user_exists(self, uid, force_update=True):
        if force_update:
            self.copy(TelegramToUsername.load_from_file(logging=False))
        return uid in self.map.keys()

    def dump_to_file(self, logging=True):
        with open(self.path, 'w', encoding='utf-8') as fout:
            for uid, username in self.map.items():
                print(uid, username, file=fout)
        if logging:
            logger.log(ADMIN_NAME, Action.DUMP_TELEGRAM_UIDS, True)

    def load_from_file(logging=True):
        try:
            target = TelegramToUsername(init_from_file=False, logging=False)
            with open(target.path, 'r', encoding='utf-8') as fin:
                for line in fin:
                    uid, username = line.strip().split()
                    uid = int(uid)
                    target.map[uid] = username
            if logging:
                logger.log(ADMIN_NAME, Action.LOAD_TELEGRAM_UIDS, True)
            return target
        except:  # syntax error in file
            if logging:
                logger.log(ADMIN_NAME, Action.LOAD_TELEGRAM_UIDS, False, "COULD_NOT_PARSE")
            raise IOError("Couldn't parse file as TelegramToUsername")

    def add_user(self, uid, username, force_update=True, logging=True):
        try:
            if force_update:
                self.copy(TelegramToUsername.load_from_file(logging=False))
            self.map[uid] = username
            self.dump_to_file(logging=False)
            if logging:
                logger.log(username, Action.ADD_USER_TELEGRAM_UID, True, str(uid))
        except:  # shouldn't cause any problems!
            if logging:
                logger.log(username, Action.ADD_USER_TELEGRAM_UID, False, "UNKNOWN_PROBLEM")

    def get_username(self, uid, force_update=True, logging=True):
        try:
            if force_update:
                self.copy(TelegramToUsername.load_from_file(logging=False))
            username = self.map[uid]
            if logging:
                logger.log(str(uid), Action.GET_USERNAME_FROM_TELEGRAM_UID, True, username)
            return username
        except KeyError:  # no such telegram uid yet
            if logging:
                logger.log(str(uid), Action.GET_USERNAME_FROM_TELEGRAM_UID, False, "UNKNOWN_TELEGRAM_UID")
            raise KeyError(f"Telegram UID {uid} was not found in DB")

telegram_uid_to_username = TelegramToUsername()


class UserState:
    def __init__(self,
                 username,
                 state=State.START,
                 lang=Lang.RUS,
                 achDone=[False for _ in range(15 + 1)],
                 lvlDone=[False for _ in range(17 + 1)],
                 treasureLvl15=[False for _ in range(24)],
                 cntLoseLvl9=0,
                 gimmeacredit=False,
                 musicVolume=100.0,
                 soundVolume=100.0,
                 unlockedFacts=False,
                 fact_idx=0):
        self.username = username
        self.state = state
        self.lang = lang
        self.achDone = deepcopy(achDone)
        self.lvlDone = deepcopy(lvlDone)
        self.treasureLvl15 = deepcopy(treasureLvl15)
        self.cntLoseLvl9 = cntLoseLvl9
        self.gimmeacredit = gimmeacredit
        self.musicVolume = musicVolume
        self.soundVolume = soundVolume
        self.unlockedFacts = unlockedFacts
        self.fact_idx = fact_idx

    def toJSON(self):
        def vector_bool_to_string(vector):
            return ''.join(str(int(elem)) for elem in vector)
        js = [self.username,
              self.state.value,
              self.lang.value,
              vector_bool_to_string(self.achDone),
              vector_bool_to_string(self.lvlDone),
              vector_bool_to_string(self.treasureLvl15),
              self.cntLoseLvl9,
              self.gimmeacredit,
              self.musicVolume,
              self.soundVolume,
              self.unlockedFacts,
              self.fact_idx,
              ]
        return json.dumps(js)

    def fromJSON(js):
        def string_to_vector_bool(string):
            return [x == '1' for x in string]
        js = json.loads(js)
        return UserState(js[0], # username
                         State(js[1]), # state
                         Lang(js[2]), # lang
                         string_to_vector_bool(js[3]), # achDone
                         string_to_vector_bool(js[4]), # lvlDone
                         string_to_vector_bool(js[5]), # treasureLvl15
                         js[6], # cntLoseLvl9
                         js[7], # gimmeacredit
                         js[8], # musicVolume
                         js[9], # soundVolume
                         js[10], # unlockedFacts
                         js[11]) # fact_idx

    def save_in_db(self, logging=True):
        try:
            with Vedis(user_db_path) as db:
                uid = username_to_db_id.get_id(self.username, logging=False)
                db[uid] = self.toJSON()
            if logging:
                logger.log(self.username, Action.SAVE_USER_IN_DB, True, str(uid))
            return True
        except:  # database problems
            if logging:
                logger.log(self.username, Action.SAVE_USER_IN_DB, False, "DB_PROBLEM")
            return False


    def load_from_db(username, logging=True):
        try:
            with Vedis(user_db_path) as db:
                uid = username_to_db_id.get_id(username, logging=False)
                userstate = UserState.fromJSON(db[uid].decode())
                if logging:
                    logger.log(username, Action.LOAD_USER_FROM_DB, True, str(uid))
                return userstate
        except:  # database problems OR no such username yet
            if logging:
                logger.log(username, Action.LOAD_USER_FROM_DB, False, "UNKNOWN_USERNAME_OR_DB_PROBLEM")
            return None


class DatabaseSelector:
    def __init__(self, logging=True):
        self.path = user_db_path
        if logging:
            logger.log(ADMIN_NAME, Action.INIT_DATABASE_SELECTOR, True)
    
    def select_users_with_ach_done(self, user, k, logging=True):
        try:
            result = []
            with Vedis(self.path) as db:
                for username in username_to_db_id.map.keys():
                    if username != ADMIN_NAME:
                        userstate = UserState.load_from_db(username, logging=False)
                        if userstate.achDone[k]:
                            result.append(username)
            result.sort()
            if logging:
                logger.log(user, Action.SELECT_USERS_WITH_ACH_DONE, True, f"{len(result)} ELEMENTS, K = {k}")
            return result
        except:  # database problems
            if logging:
                logger.log(user, Action.SELECT_USERS_WITH_ACH_DONE, False, "DB_PROBLEM")
            return None

    def select_users_with_lvl_done(self, user, k, logging=True):
        try:
            result = []
            with Vedis(self.path) as db:
                for username in username_to_db_id.map.keys():
                    if username != ADMIN_NAME:
                        userstate = UserState.load_from_db(username, logging=False)
                        if userstate.lvlDone[k]:
                            result.append(username)
            result.sort()
            if logging:
                logger.log(user, Action.SELECT_USERS_WITH_LVL_DONE, True, f"{len(result)} ELEMENTS, K = {k}")
            return result
        except:  # database problems
            if logging:
                logger.log(user, Action.SELECT_USERS_WITH_LVL_DONE, False, "DB_PROBLEM")
            return None

    def sort_users_by_ach_num(self, user, ascending=True, logging=True):
        try:
            result = []
            with Vedis(self.path) as db:
                for username in username_to_db_id.map.keys():
                    if username != ADMIN_NAME:
                        userstate = UserState.load_from_db(username, logging=False)
                        result.append((sum(userstate.achDone), username))
            if ascending:
                result.sort(key=lambda x: (x[0], x[1]))
            else:
                result.sort(key=lambda x: (-x[0], x[1]))
            if logging:
                logger.log(user,
                           Action.SORT_USERS_BY_ACH_NUM,
                           True,
                           f"{len(result)} ELEMENTS, {'ASCENDING' if ascending else 'DESCENDING'}")
            return result
        except:  # database problems
            if logging:
                logger.log(user, Action.SORT_USERS_BY_ACH_NUM, False, "DB_PROBLEM")
            return None

    def sort_users_by_lvl_num(self, user, ascending=True, logging=True):
        try:
            result = []
            with Vedis(self.path) as db:
                for username in username_to_db_id.map.keys():
                    if username != ADMIN_NAME:
                        userstate = UserState.load_from_db(username, logging=False)
                        result.append((sum(userstate.lvlDone), username))
            if ascending:
                result.sort(key=lambda x: (x[0], x[1]))
            else:
                result.sort(key=lambda x: (-x[0], x[1]))
            if logging:
                logger.log(user,
                           Action.SORT_USERS_BY_LVL_NUM,
                           True,
                           f"{len(result)} ELEMENTS, {'ASCENDING' if ascending else 'DESCENDING'}")
            return result
        except:  # database problems
            if logging:
                logger.log(user, Action.SORT_USERS_BY_LVL_NUM, False, "DB_PROBLEM")
            return None

database_selector = DatabaseSelector()

