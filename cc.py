import requests

import common


class CC:
    STAT_FAIL = 0
    STAT_SUCCESS = 1
    STAT_CLOSE = 2

    LOGIN_URL = 'http://%s/Login.aspx'
    SIGNIN_URL = 'http:/%s/cc.szpt.edu.cn/sSign.aspx'

    def __init__(self, host='cc.szpt.edu.cn'):
        self._session = requests.session()
        self.LOGIN_URL = self.LOGIN_URL % host
        self.SIGNIN_URL = self.SIGNIN_URL % host

    def login(self, username, password):
        resp = self._session.get(self.LOGIN_URL)
        fs = common.extract_forms(resp.text)
        if len(fs) > 0:
            f = fs[0]
            data = common.generate_data(f['inputs'])
            data['TextBoxTeacherName'] = username
            data['TextBoxPassword'] = password
            resp = self._session.post(self.LOGIN_URL, data)
            return 'Logined' in resp.url
        else:
            return False

    def signin(self):
        resp = self._session.get(self.SIGNIN_URL)
        fs = common.extract_forms(resp.text)
        if len(fs) > 0:
            f = fs[0]
            data = common.generate_data(f['inputs'])
            resp = self._session.post(self.SIGNIN_URL, data)
            if '签到成功' in resp.text:
                return CC.STAT_SUCCESS
            elif '签到未开通' in resp.text:
                return CC.STAT_CLOSE
            else:
                return CC.STAT_FAIL
        else:
            return CC.STAT_FAIL
