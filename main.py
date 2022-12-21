# -*- coding: utf-8 -*-

from bot import bot_main
from database import cloud_upload_files
from server import server_main

from threading import Thread, Lock
from time import sleep


def backup_main(lock):
    while True:
        sleep(60 * 20)  # 20 minutes
        with lock:
            cloud_upload_files()


if __name__ == '__main__':
    lock = Lock()

    bot_job = Thread(target=bot_main, args=(lock,))
    server_job = Thread(target=server_main, args=(lock,))
    backup_job = Thread(target=backup_main, args=(lock,))

    bot_job.start()
    server_job.start()
    backup_job.start()
