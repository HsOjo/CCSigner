import json
import os
import sys
import time
import traceback

from cc import CC

FILE_ACCOUNT = './account.json'

try:
    config = {
        'username': '',
        'password': '',
        'interval': 1,
        'type': 1,  # 1.normal 2.mobile 3.vpn
        'protocol': 'http',
        'start_now': False,
    }

    if len(sys.argv) > 1:
        FILE_ACCOUNT = sys.argv[1]

    if os.path.exists(FILE_ACCOUNT):
        with open(FILE_ACCOUNT, 'r', encoding='utf8') as io:
            config.update(**json.load(io))
        print('Init.', config)
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

    if not config['start_now']:
        try:
            sleep_time = int(input('Input sleep time(seconds):'))
            time.sleep(sleep_time)
        except:
            pass

    cc = CC(config.get('host'), auth=auth, protocol=config.get('protocol'))
    if cc.login(config['username'], config['password']):
        print('Login success.')
        i = 0
        while True:
            if config['type'] == 2:
                r = cc.signin_mobile(config['username'])
            elif config['type'] == 3:
                r = cc.signin_vpn()
            else:
                r = cc.signin()
            if r == CC.STAT_SUCCESS:
                print('Signin success.')
                break
            elif r == CC.STAT_CLOSE:
                print(('[%s] Signin closed, retry' % i) + ('.' * (i % 4)) + (' ' * 3), end='\r')
            else:
                print('[%s] Signin failed, retry.' % i)

            time.sleep(config['interval'])

            i += 1
    else:
        print('Login failed.')
except KeyboardInterrupt:
    print()
except:
    traceback.print_exc()
finally:
    input('Stopped.')
