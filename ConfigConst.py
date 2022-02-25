# 数据库相关
HOST = "api.mapotofu.cn"
PORT = 3306
USER = "user_yqfk_v1"
PSWD = "TAjt2SfRtRF7JaHX"
DB_NAME = "user_yqfk_v1"

# 学校疫情防控URL
BASE_URL = "http://yqfk.wsyu.edu.cn:8089"
URL_LOGIN = "/appLogin/login"
URL_GET_USER_INFO = "/appWX/getUserInfo"
URL_ADD_HEALTH_QUESTIONNAIRE = "/hltQstnr/addHltQstnr"
URL_SELECT_HEALTH_QUESTIONNAIRE_ADDR = "/hltQstnr/selectHltQstnrAddress"

# 设置相关
TIMEOUT = 5
USER_AGENT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.4_android_phone_614_74"
LOCATION = "湖北省武汉市"
HEALTH_FORM_STATE = "2,2,2,"

# 文案
TEXT_MAX_TRIES = "已尝试三次登陆，均失败，遂放弃尝试，错误已写入日志。"
TEXT_USER_NOT_EXIST = "用户不存在～"
TEXT_WRONG_PASSWORD = "密码不正确～"
TEXT_SUCCESS_DELETE = "删除用户成功～"
TEXT_INDEX = "这里是首义学院疫情防控自动打卡API～"
