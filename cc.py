import requests

import common


class CC:
    STAT_FAIL = 0
    STAT_SUCCESS = 1
    STAT_CLOSE = 2

    LOGIN_URL = 'http://cc.szpt.edu.cn/Login.aspx'
    SIGNIN_URL = 'http://cc.szpt.edu.cn/sSign.aspx'

    def __init__(self):
        self._session = requests.session()

    def login(self, username, password):
        resp = self._session.get(CC.LOGIN_URL)
        fs = common.extract_forms(resp.text)
        if len(fs) > 0:
            f = fs[0]
            data = common.generate_data(f['inputs'])
            data['TextBoxTeacherName'] = username
            data['TextBoxPassword'] = password
            resp = self._session.post(CC.LOGIN_URL, data)
            return 'Logined' in resp.url
        else:
            return False

    def signin(self):
        resp = self._session.get(CC.SIGNIN_URL)
        fs = common.extract_forms(resp.text)
        if len(fs) > 0:
            f = fs[0]
            data = common.generate_data(f['inputs'])
            resp = self._session.post(CC.SIGNIN_URL, data)
            if '签到成功' in resp.text:
                return CC.STAT_SUCCESS
            elif '签到未开通' in resp.text:
                return CC.STAT_CLOSE
            else:
                return CC.STAT_FAIL
        else:
            return CC.STAT_FAIL
