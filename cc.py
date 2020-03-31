import random
import re
from urllib.parse import parse_qs

import requests

import common


class CC:
    STAT_FAIL = 0
    STAT_SUCCESS = 1
    STAT_CLOSE = 2

    LOGIN_URL = 'http://%s/Login.aspx'
    SIGNIN_URL = 'http://%s/sSign.aspx'
    SIGNIN_MOBILE_PORTAL_URL = 'http://%s/m/SignM.aspx'
    SIGNIN_MOBILE_URL = 'http://%s/m/SignCct.aspx'

    def __init__(self, host='cc.szpt.edu.cn'):
        self._session = requests.session()
        self.LOGIN_URL = self.LOGIN_URL % host
        self.SIGNIN_URL = self.SIGNIN_URL % host
        self.SIGNIN_MOBILE_PORTAL_URL = self.SIGNIN_MOBILE_PORTAL_URL % host
        self.SIGNIN_MOBILE_URL = self.SIGNIN_MOBILE_URL % host

    def extract_form(self, content, index=0):
        fs = common.extract_forms(content)
        if len(fs) > index:
            f = fs[index]
            data = common.generate_data(f['inputs'])
            return data
        else:
            return None

    def login(self, username, password):
        resp = self._session.get(self.LOGIN_URL)
        data = self.extract_form(resp.text)
        if data is not None:
            data['TextBoxTeacherName'] = username
            data['TextBoxPassword'] = password
            resp = self._session.post(self.LOGIN_URL, data)
            return 'Logined' in resp.url
        else:
            return False

    def signin(self):
        resp = self._session.get(self.SIGNIN_URL)
        data = self.extract_form(resp.text)
        if data is not None:
            resp = self._session.post(self.SIGNIN_URL, data)
            if '签到成功' in resp.text:
                return CC.STAT_SUCCESS
            elif '签到未开通' in resp.text:
                return CC.STAT_CLOSE
            else:
                return CC.STAT_FAIL
        else:
            return CC.STAT_FAIL

    def signin_mobile(self, username):
        resp = self._session.get(self.SIGNIN_MOBILE_PORTAL_URL)
        data = self.extract_form(resp.text)
        if data is not None:
            data['TextBoxNameNo'] = username
            resp = self._session.post(self.SIGNIN_MOBILE_PORTAL_URL, data)
            content = resp.text
            if 'SignCct' in content:
                return self._signin_mobile(resp)
            elif '老师尚未开通签到' in content:
                return CC.STAT_CLOSE
            else:
                return CC.STAT_FAIL
        else:
            return CC.STAT_FAIL

    def _signin_mobile(self, resp_portal):
        content = resp_portal.text

        reg_params = re.compile("window.location.href='SignCct\.aspx\?(.*?)'")
        params = reg_params.findall(content)
        if len(params) >= 1:
            params = parse_qs(params[0])
            params = dict([(k, v[0]) for k, v in params.items()])

        resp = self._session.get(self.SIGNIN_MOBILE_URL, params=params)
        content = resp.text
        data = {}

        positions = []
        reg_positions_2 = re.compile(
            r'<span id="DataList1_LabelStudentName_(\d+)" title="学号: " style="color:Blue;"></span>')
        indexes = reg_positions_2.findall(content)
        for index in indexes:
            reg_position = re.compile(r'<span id="DataList1_LabelDesk_%s">-\D*(\d\.\d\.\d)\D*?-</span>' % index)
            position = reg_position.findall(content)
            if len(position) > 0:
                positions.append(position[0])

        if len(positions) != 0:
            position = positions[random.randint(0, len(positions) - 1)]
            data['TextBoxDesk'] = position
            resp = self._session.post(self.SIGNIN_MOBILE_URL, data, params=params)
            if '签到成功' in resp.text:
                return CC.STAT_SUCCESS
            else:
                return CC.STAT_CLOSE
        else:
            return CC.STAT_FAIL
