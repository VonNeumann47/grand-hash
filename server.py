# -*- coding: utf-8 -*-

from config import Action, ADMIN_NAME, HOST, PORT
from database import UserState, \
                     logger, username_to_db_id, telegram_uid_to_username, database_selector, \
                     cloud_download_files

from datetime import datetime
from flask import Flask, make_response
import json
import pytz


lock = 0
app = Flask(__name__)


@app.route('/ping/')
def ping():
    with lock:
        cloud_download_files()
        logger.log(ADMIN_NAME, Action.SERVER_PING, True)
        return make_response("[]", 200)


@app.route('/timehour/<string:username>/')
def timehour(username):
    with lock:
        cloud_download_files()
        tz = pytz.timezone('Europe/Moscow')
        dt = datetime.now(tz)
        logger.log(username, Action.SERVER_TIME, True, str(dt))
        return make_response(f"{dt.hour}", 200)


@app.route('/signin/<string:username>/')
def sign_in(username):
    with lock:
        cloud_download_files()
        userstate = UserState.load_from_db(username)
        if userstate is None:
            logger.log(username, Action.SERVER_SIGN_IN, False, "UNKNOWN_USERNAME")
            return make_response("null", 400)
        js = userstate.toJSON()
        logger.log(username, Action.SERVER_SIGN_IN, True)
        return make_response(js, 200)


@app.route('/createuser/<string:username>/')
def create_user(username):
    with lock:
        cloud_download_files()
        try:
            username_to_db_id.add_user(username)
            logger.log(username, Action.SERVER_CREATE_USER, True)
            return make_response("OK", 200)
        except:
            logger.log(username, Action.SERVER_CREATE_USER, False, "USER_ALREADY_EXISTS")
            return make_response("null", 400)


@app.route('/savegame/<string:js>/')
def save_game(js):
    with lock:
        cloud_download_files()
        try:
            userstate = UserState.fromJSON(js)
            username = userstate.username
            us_old = UserState.load_from_db(username)

            userstate.state = us_old.state
            userstate.lang = us_old.lang
            userstate.unlockedFacts = us_old.unlockedFacts
            userstate.fact_idx = us_old.fact_idx

            userstate.save_in_db()
            logger.log(username, Action.SERVER_SAVE_GAME, True)
            return make_response("OK", 200)
        except:
            logger.log(ADMIN_NAME, Action.SERVER_SAVE_GAME, False, js)
            return make_response("null", 400)


@app.route('/loadgame/<string:username>/')
def load_game(username):
    with lock:
        cloud_download_files()
        try:
            userstate = UserState.load_from_db(username)
            js = userstate.toJSON()
            logger.log(username, Action.SERVER_LOAD_GAME, True)
            return make_response(js, 200)
        except:
            logger.log(username, Action.SERVER_LOAD_GAME, False, "UNKNOWN_USERNAME")
            return make_response("null", 400)


@app.route('/selectach/<string:user>/<int:k>/')
def select_ach(user, k):
    with lock:
        cloud_download_files()
        try:
            result = database_selector.select_users_with_ach_done(user, k)
            return make_response(json.dumps(result), 200)
        except:
            return make_response("null", 400)


@app.route('/selectlvl/<string:user>/<int:k>/')
def select_lvl(user, k):
    with lock:
        cloud_download_files()
        try:
            result = database_selector.select_users_with_lvl_done(user, k)
            return make_response(json.dumps(result), 200)
        except:
            return make_response("null", 400)


@app.route('/sortach/<string:user>/<int:ascending>/')
def sort_ach(user, ascending):
    with lock:
        cloud_download_files()
        try:
            result = database_selector.sort_users_by_ach_num(user, ascending)
            return make_response(json.dumps(result), 200)
        except:
            return make_response("null", 400)


@app.route('/sortlvl/<string:user>/<int:ascending>/')
def sort_lvl(user, ascending):
    with lock:
        cloud_download_files()
        try:
            result = database_selector.sort_users_by_lvl_num(user, ascending)
            return make_response(json.dumps(result), 200)
        except:
            return make_response("null", 400)


def server_main(main_lock):
    global lock
    lock = main_lock
    app.run(host=HOST, port=PORT)
