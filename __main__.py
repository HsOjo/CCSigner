import json
import os
import time
import traceback

from cc import CC

FILE_ACCOUNT = './account.json'

try:
    c = CC()

    if os.path.exists(FILE_ACCOUNT):
        with open(FILE_ACCOUNT, 'r', encoding='utf8') as io:
            account = json.load(io)
    else:
        account = {
            'username': input('Username:'),
            'password': input('Password:'),
        }
        with open(FILE_ACCOUNT, 'w', encoding='utf8') as io:
            json.dump(account, io, ensure_ascii=False, indent=4)

    if c.login(**account):
        print('Login success.')
        while True:
            r = c.signin()
            if r == CC.STAT_SUCCESS:
                print('Signin success.')
                break
            elif r == CC.STAT_CLOSE:
                print('Signin closed, retry.')
            else:
                print('Signin failed, retry.')

            time.sleep(1)
    else:
        print('Login failed.')
except:
    traceback.print_exc()
finally:
    input('Pause.')
