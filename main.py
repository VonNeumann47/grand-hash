# -*- coding: utf-8 -*-

from bot import bot_main
from server import server_main

from threading import Thread, Lock


if __name__ == '__main__':
    lock = Lock()
    
    bot_job = Thread(target=bot_main, args=(lock,))
    server_job = Thread(target=server_main, args=(lock,))

    bot_job.start()
    server_job.start()

