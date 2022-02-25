from urllib.parse import urljoin

import requests

from ConfigConst import *


def build_state(data: dict):
    """
    返回api状态码
    :param data: 数据
    :return: {状态码，消息，数据}，其中状态码200为正常，400为不正常
    """
    if data['code'] == "00":
        return {'code': 200, 'msg': data['message'], 'data': data}
    else:
        return {'code': 400, 'msg': data['message'], 'data': data}


class ClockIn(object):
    def __init__(self):
        self.login_url = urljoin(BASE_URL, URL_LOGIN)
        self.user_info_url = urljoin(BASE_URL, URL_GET_USER_INFO)
        self.health_questionnaire_url = urljoin(BASE_URL, URL_ADD_HEALTH_QUESTIONNAIRE)
        self.select_health_questionnaire_addr_url = urljoin(BASE_URL, URL_SELECT_HEALTH_QUESTIONNAIRE_ADDR)
        self.headers = requests.utils.default_headers()
        self.headers["Referer"] = self.login_url
        self.headers["User-Agent"] = USER_AGENT
        self.headers["Accept"] = "*/*"
        self.sess = requests.Session()
        self.sess.keep_alive = True
        self.cookies = {}

    def get_uuid(self, username: str, password: str):
        """
        获取用户UUID
        :param username: 学号
        :param password: 姓名
        :return: dict
        """
        data = self.sess.post(
            self.login_url,
            headers=self.headers,
            json={'username': username, 'password': password},
            timeout=TIMEOUT
        ).json()
        if data['code'] == "00":
            self.cookies = {'JSESSIONID': data['data']['JSESSIONID']}
        return build_state(data)

    def get_userinfo(self, uuid: str):
        """
        获取用户基本信息， 其中data字段里，hltSt==1为已填报，hltSt==2为未填报
        :param uuid: UUID
        :return: dict
        """
        data = self.sess.post(
            self.user_info_url,
            headers=self.headers,
            json={'UUID': uuid},
            timeout=TIMEOUT
        ).json()
        return build_state(data)

    def get_addr(self, uuid):
        """
        获取上一次填报地址
        :param uuid: UUID
        :return: dict
        """
        data = self.sess.post(
            self.select_health_questionnaire_addr_url,
            headers=self.headers,
            json={'UUID': uuid},
            timeout=TIMEOUT
        ).json()
        return build_state(data)

    def post_health_form(self, uuid: str, addr: str = '', ansr: str = HEALTH_FORM_ANSWER):
        """
        发送疫情打卡表单
        :param uuid: UUID
        :param addr: 位置
        :param ansr: 问卷回答
        :return: dict
        """
        # 首选上次填报地址
        last_select_addr = self.get_addr(uuid)
        data = self.sess.post(
            self.health_questionnaire_url,
            headers=self.headers,
            json={
                'ansr': ansr,
                'address': last_select_addr['data']['data'] if last_select_addr['code'] == 200 else DEFAULT_LOCATION,
                'uuid': uuid
            },
            timeout=TIMEOUT
        ).json()
        return build_state(data)

    def one_click_clock_in(self, username: str, password: str):
        """
        一键打卡
        :param username: 学号
        :param password: 姓名
        :return: dict
        """
        uuid_data = self.get_uuid(username, password)
        uuid = uuid_data['data']['data']['uuid']
        if uuid_data['code'] == 400:
            # 直接返回错误消息
            return uuid_data
        if uuid_data['code'] == 200:
            # 登录成功
            health_question_result = self.post_health_form(uuid)
            user_info = self.get_userinfo(uuid)
            if user_info['data']['data']['hltSt'] == "1":
                # 手动将状态码改为200
                health_question_result['code'] = 200
            return health_question_result
