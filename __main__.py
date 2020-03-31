import json
import os
import time
import traceback

from cc import CC

FILE_ACCOUNT = './account.json'

try:
    c = CC()
    config = {
        'username': '',
        'password': '',
        'interval': 1,
        'mobile': True,
    }

    if os.path.exists(FILE_ACCOUNT):
        with open(FILE_ACCOUNT, 'r', encoding='utf8') as io:
            config.update(**json.load(io))
    else:
        config.update(
            username=input('Username:'),
            password=input('Password:'),
        )
        with open(FILE_ACCOUNT, 'w', encoding='utf8') as io:
            json.dump(config, io, ensure_ascii=False, indent=4)

    if config['mobile']:
        while True:
            r = c.signin_mobile(config['username'])
            if r == CC.STAT_SUCCESS:
                print('Signin success.')
                break
            elif r == CC.STAT_CLOSE:
                print('Signin closed, retry.')
            else:
                print('Signin failed, retry.')

            time.sleep(config['interval'])
    else:
        if c.login(**config):
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

                time.sleep(config['interval'])
        else:
            print('Login failed.')
except:
    traceback.print_exc()
finally:
    input('Pause.')
