# -*- coding: utf-8 -*-

from config import State, Lang, Action, \
                   ADMIN_NAME, TELEGRAM_TOKEN
from database import UserState, \
                     logger, username_to_db_id, telegram_uid_to_username, database_selector, \
                     cloud_download_files
from talks import talks_dict, facts_dict, secret_pass, key_phrases, \
                  normalize_text, reEscapeString, is_word_in, \
                  is_lang_rus, is_lang_eng, \
                  is_offensive, is_question, is_thanks, is_greeting, is_bye

import telebot as tb


def hash_username_lvl17(name):
    MAX_LEN = 25
    hashSymbols = ["abcdefghijklmnopqrstuvwxyz",
                   "0123456789",
                   "!@#$%^&*\"'",
                   "-_=+,.?:;",
                   "[{]}<>()",
                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                   "/|\\",
                   "'\"*&^%$#@!",
                   ";:?.,+=_-",
                   "3827591460",
                   "zyxwvutsrqponmlkjihgfedcba",
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA",
                   ]
    result = 'F' * MAX_LEN
    for i in range(MAX_LEN):
        hs = hashSymbols[i % len(hashSymbols)]
        result = result[:i] + hs[ord(name[i % len(name)]) % len(hs)] + result[i + 1:]
    L = max(10, (len(name) + ord(name[3]) - ord(name[1]) + 42 + MAX_LEN * 7) % MAX_LEN)
    S = (ord(name[2]) * 3 - ord(name[0]) + ord(name[-1])) % (MAX_LEN - L)
    return result[S:S + L]


def hash_username_secret_facts(name):
    MAX_LEN = 12
    hashSymbols = ["0123456789",
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA",
                   "-_=+,.:;",
                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                   "!@#$%^&*\"'",
                   "abcdefghijklmnopqrstuvwxyz",
                   "3827591460",
                   "/|\\",
                   "zyxwvutsrqponmlkjihgfedcba",
                   "[{]}<>()",
                   "'\"*&^%$#@!",
                   ";:.,+=_-",
                   ]
    result = 'F' * MAX_LEN
    for i in range(MAX_LEN):
        hs = hashSymbols[i % len(hashSymbols)]
        result = result[:i] + hs[ord(name[i % len(name)]) % len(hs)] + result[i + 1:]
    return result


lock = 0
bot = tb.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(content_types=['sticker', 'photo', 'voice'])
def strange_content(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        try:
            username = telegram_uid_to_username.get_username(uid)
            userstate = UserState.load_from_db(username)
            lang = userstate.lang.value
            bot.send_message(uid, talks_dict[lang]["strange_content"])
            logger.log(username, Action.SENT_STRANGE_CONTENT, True, str(uid))
        except:  # unknown user -> ignore
            logger.log(ADMIN_NAME, Action.SENT_STRANGE_CONTENT, False, str(uid))


@bot.message_handler(commands=['start', 'restart'])
def on_start(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        lang = Lang.ENG.value
        if not telegram_uid_to_username.user_exists(uid):
            telegram_uid_to_username.add_user(uid, "N/A")
            logger.log(ADMIN_NAME, Action.ADD_NEW_TELEGRAM_UID, True, str(uid))
        else:
            username = telegram_uid_to_username.get_username(uid)
            userstate = UserState.load_from_db(username)
            lang = userstate.lang.value
            userstate.state = State.INPUT_NAME
            userstate.save_in_db()
            logger.log(username, Action.TELEGRAM_COMMAND_START, True, str(uid))
        bot.send_message(uid, talks_dict[lang]["start"])
        


@bot.message_handler(commands=['help'])
def on_help(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        try:
            username = telegram_uid_to_username.get_username(uid)
            userstate = UserState.load_from_db(username)
            lang = userstate.lang.value
            state = userstate.state.value

            if state == State.HANDLE_FORK.value or state == State.SECRET_HANDLE_FORK.value:
                bot.send_message(uid, facts_dict[lang]["fork"])
            logger.log(username, Action.TELEGRAM_COMMAND_HELP, True, str(uid))
        except:  # unknown user -> ignore
            bot.send_message(uid, "Gotta ignore you until we get acquainted.")
            logger.log(ADMIN_NAME, Action.TELEGRAM_COMMAND_HELP, False, "UNKNOWN_TELEGRAM_UID")


@bot.message_handler(commands=['exit', 'quit', 'runaway', 'getout'])
def on_exit(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        try:
            username = telegram_uid_to_username.get_username(uid)
            userstate = UserState.load_from_db(username)
            lang = userstate.lang.value
            userstate.state = State.START
            bot.send_message(uid, facts_dict[lang]["bye"])
            userstate.save_in_db()
            logger.log(username, Action.TELEGRAM_COMMAND_EXIT, True, str(uid))
        except:  # unknown user -> ignore
            bot.send_message(uid, "Gotta ignore you until we get acquainted.")
            logger.log(ADMIN_NAME, Action.TELEGRAM_COMMAND_EXIT, False, "UNKNOWN_TELEGRAM_UID")


@bot.message_handler(commands=['info', 'random', 'talk'])
def on_info(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        try:
            username = telegram_uid_to_username.get_username(uid)
            userstate = UserState.load_from_db(username)
            lang = userstate.lang.value
            state = userstate.state.value

            if state != State.SECRET_HANDLE_FORK.value:
                bot.send_message(uid, talks_dict[lang]["trash"])
                return

            bot.send_message(uid, facts_dict[lang][userstate.fact_idx])
            userstate.fact_idx = (userstate.fact_idx + 1) % len(facts_dict[lang])
            userstate.save_in_db()
            logger.log(username, Action.TELEGRAM_COMMAND_INFO, True, str(uid))
        except:  # unknown user -> ignore
            bot.send_message(uid, "Gotta ignore you until we get acquainted.")
            logger.log(ADMIN_NAME, Action.TELEGRAM_COMMAND_INFO, False, "UNKNOWN_TELEGRAM_UID")


@bot.message_handler(func=lambda x: True)  # lambda?
def on_talking(message):
    with lock:
        cloud_download_files()
        uid = message.chat.id
        if not telegram_uid_to_username.user_exists(uid): # unknown telegram uid -> ignore
            bot.send_message(uid, "Gotta ignore you until we get acquainted.")
            logger.log(ADMIN_NAME, Action.TELEGRAM_TALKING, False, "UNKNOWN_TELEGRAM_UID")
            return
        
        username = telegram_uid_to_username.get_username(uid)
        logger.log(username, Action.TELEGRAM_TALKING, True, str(uid))
        if username == "N/A":
            username = message.text
            if username != ADMIN_NAME and username_to_db_id.user_exists(username):
                telegram_uid_to_username.add_user(uid, username)
                userstate = UserState.load_from_db(username)
                bot.send_message(uid, talks_dict[Lang.ENG.value]["lang"])
                userstate.state = State.CHOOSE_LANG
                userstate.save_in_db()
                logger.log(username, Action.TELEGRAM_FIRST_ENTER, True, str(uid))
            else:
                bot.send_message(uid, talks_dict[Lang.ENG.value]["start_again"])
                logger.log(str(uid), Action.TELEGRAM_FIRST_ENTER, False, "UNKNOWN_USERNAME")
            return
        
        userstate = UserState.load_from_db(username)
        lang = userstate.lang.value
        state = userstate.state.value
        input = message.text

        if state == State.INPUT_NAME.value:
            name = input
            if name != ADMIN_NAME and username_to_db_id.user_exists(name):
                telegram_uid_to_username.add_user(uid, name)
                userstate = UserState.load_from_db(name)
                lang = userstate.lang.value
                bot.send_message(uid, talks_dict[lang]["lang"])
                userstate.state = State.CHOOSE_LANG
                userstate.save_in_db()
                logger.log(name, Action.TELEGRAM_INPUT_NAME, True, str(uid))
            else:
                bot.send_message(uid, talks_dict[lang]["start_again"])
                logger.log(str(uid), Action.TELEGRAM_INPUT_NAME, False, "UNKNOWN_USERNAME")
        elif state == State.CHOOSE_LANG.value:
            if is_lang_rus(input):
                userstate.lang = Lang.RUS
            elif is_lang_eng(input):
                userstate.lang = Lang.ENG
            else:
                bot.send_message(uid, talks_dict[lang]["lang_again"])
                logger.log(userstate.username, Action.TELEGRAM_CHOOSE_LANG, False, input)
                return
            userstate.state = State.SECRET_HANDLE_FORK if userstate.unlockedFacts else State.HANDLE_FORK
            bot.send_message(uid, talks_dict[userstate.lang.value]["fork"])
            userstate.save_in_db()
            logger.log(userstate.username, Action.TELEGRAM_CHOOSE_LANG, True, userstate.lang.name)
        elif state == State.HANDLE_FORK.value or state == State.SECRET_HANDLE_FORK.value:
            normalized = normalize_text(input)
            if input == hash_username_secret_facts(username):
                if state != State.SECRET_HANDLE_FORK.value:
                    userstate.state = State.SECRET_HANDLE_FORK
                    userstate.unlockedFacts = True
                    bot.send_message(uid, talks_dict[lang]["secret_found"])
                    userstate.save_in_db()
                    logger.log(userstate.username, Action.TELEGRAM_SECRETS_UNLOCKED, True, input)
                else:
                    bot.send_message(uid, talks_dict[lang]["trash"])
                    logger.log(userstate.username, Action.TELEGRAM_SECRETS_UNLOCKED, False, input)
            elif is_offensive(normalize_text(input, specials="&*!.)_($+-'/")):
                bot.send_message(uid, talks_dict[lang]["offensive"])
                logger.log(userstate.username, Action.TELEGRAM_OFFENSIVE, True, input)
            elif is_question(normalized):
                bot.send_message(uid, talks_dict[lang]["question"])
                logger.log(userstate.username, Action.TELEGRAM_QUESTION, True, input)
            elif is_thanks(normalized):
                bot.send_message(uid, talks_dict[lang]["thanks"])
                logger.log(userstate.username, Action.TELEGRAM_THANKS, True, input)
            elif is_greeting(normalized):
                bot.send_message(uid, talks_dict[lang]["greeting"])
                logger.log(userstate.username, Action.TELEGRAM_GREETING, True, input)
            elif is_bye(normalized):
                bot.send_message(uid, talks_dict[lang]["bye"])
                logger.log(userstate.username, Action.TELEGRAM_BYE, True, input)
            elif normalized == secret_pass[lang]:
                bot.send_message(uid, hash_username_lvl17(username))
                logger.log(userstate.username, Action.TELEGRAM_LEVEL_17, True, input)
            else:
                for word in key_phrases[lang].keys():
                    if is_word_in(input, word):
                        bot.send_message(uid, key_phrases[lang][f"{word}"])
                        logger.log(userstate.username, Action.TELEGRAM_KEY_PHRASE, True, input)
                        break
                else:
                    bot.send_message(uid, talks_dict[lang]["trash"])
                    logger.log(userstate.username, Action.TELEGRAM_TRASH, True, input)


def bot_main(main_lock):
    global lock
    lock = main_lock
    bot.polling(none_stop=True)


