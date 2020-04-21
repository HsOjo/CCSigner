import json
import os
import time
import traceback

from cc import CC

FILE_ACCOUNT = './account.json'

try:
    config = {
        'username': '',
        'password': '',
        'interval': 1,
        'mobile': True,
        'protocol': 'http',
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

    auth = config.get('auth')
    if auth is not None:
        auth = tuple(auth)

    cc = CC(config.get('host'), auth=auth, protocol=config.get('protocol'))
    if cc.login(config['username'], config['password']):
        print('Login success.')
        while True:
            if config['mobile']:
                r = cc.signin_mobile(config['username'])
            else:
                r = cc.signin()
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
