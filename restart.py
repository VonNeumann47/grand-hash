from config import log_path, known_users_path, telegram_uids_path, user_db_path, \
                   ADMIN_NAME
from database import cloud_upload_files

from vedis import Vedis


def deleteContent(path):
    with open(path, 'w'):
        pass


deleteContent(telegram_uids_path)

with open(known_users_path, 'w', encoding='utf-8') as fout:
    print('$ADMIN$ 0', file=fout)

with open(log_path, 'w', encoding='utf-8') as fout:
    print("Username".center(15),
          "Action type".center(30),
          "Success".center(10),
          "Timestamp".center(15),
          "Additional information".center(30),

          sep='|',
          file=fout)
    print("-" * 104, file=fout)

with open(user_db_path, 'w'):
    pass
with Vedis(user_db_path) as db:    
    db[0] = ADMIN_NAME


cloud_upload_files()

