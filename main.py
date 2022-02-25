import os

from fastapi import FastAPI, Depends, Request
from sqlalchemy import exists
from sqlalchemy.orm import Session
from datetime import datetime
from requests import exceptions
import traceback

from api_wsyu_yqfk import ClockIn
from database.database import SessionLocal
from database.models import UserInfo
from ConfigConst import *

app = FastAPI(debug=True, docs_url="/docsss")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 写log函数
def write_log(content):
    date = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists('logssss'):
        os.mkdir('logssss')

    def write():
        file_name = 'logssss/' + date + '.log'
        if not os.path.exists(file_name):
            with open(file_name, mode='w', encoding='utf-8') as n:
                n.write('【%s】的日志记录' % date)
        with open(file_name, mode='a', encoding='utf-8') as l:
            l.write('\n%s' % content)

    write()


# 写error_log函数
def write_exception_log(content):
    date = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists('logssss_error'):
        os.mkdir('logssss_error')

    def write():
        file_name = 'logssss_error/' + date + '.log'
        if not os.path.exists(file_name):
            with open(file_name, mode='w', encoding='utf-8') as n:
                n.write('【%s】的抛出错误日志记录' % date)
        with open(file_name, mode='a', encoding='utf-8') as l:
            l.write('\n%s' % content)
            l.write(f"\n----------俺是分割线～----------[{datetime.now().strftime('%H:%M:%S')}]-------------")

    write()


@app.post('/clock_in')
async def check(request: Request, db: Session = Depends(get_db), username: str = '', password: str = ''):
    if username == '' or password == '':
        return {"code": 400, "msg": "缺少参数", "data": {}}
    try:
        # 用户是否存在
        user_exists = db.query(exists().where(UserInfo.student_id == username)).scalar()
        # 开始登陆
        lgn = ClockIn()
        result = lgn.one_click_clock_in(username, password)
        # 如果打卡成功且不再数据库内，则进行入库
        if result['code'] == 200 and not user_exists:
            student = UserInfo(student_id=username, name=password, last_clockin=datetime.now())
            db.add(student)
            db.commit()
            write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]首次登陆使用，进行入库操作")
            return result
        if result['code'] == 200:
            # 提交成功
            db.query(UserInfo).filter(UserInfo.student_id == username).update(
                {'last_clockin': datetime.now()}
            )
            db.commit()
            write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]打卡成功")
            return result
        if result['code'] == 400:
            # 提交失败，将尝试重新提交，若重试次数超过三次则放弃，并写入日志
            write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]记录到一次失败，原因为[{result['msg']}]")
            write_exception_log(result)
            return result

    except exceptions.Timeout:
        write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]打卡时Timeout")
        return {"code": 400, "msg": "登录超时", "data": {}}
    except exceptions.RequestException:
        write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]打卡时RequestException")
        return {"code": 400, "msg": "系统维护中", "data": {}}
    except Exception as e:
        traceback.print_exc()
        write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]打卡时触发未记录的错误，已保存错误日志")
        write_exception_log(str(e))
        return {"code": 400, "msg": "未记录的错误：" + str(e), "data": {}}


@app.post("/delete_user")
async def delete(request: Request, db: Session = Depends(get_db), username: str = '', password: str = ''):
    if username == '' or password == '':
        return {"code": 400, "msg": "缺少参数", "data": {}}
    # 用户是否存在
    if db.query(exists().where(UserInfo.student_id == username)).scalar():
        # 判断密码是否一致
        item = db.query(UserInfo.name).filter(UserInfo.name == password).first()
        if item:
            db.query(UserInfo).filter(UserInfo.student_id == username).delete()
            db.commit()
            write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]进行了删除用户操作")
            return {"code": 200, "msg": TEXT_SUCCESS_DELETE, "data": {}}
        else:
            write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]进行了删除用户操作，但密码不正确")
            return {"code": 400, "msg": TEXT_WRONG_PASSWORD, "data": {}}
    else:
        write_log(f"({datetime.now().strftime('%H:%M:%S')})[{username}&{password}]想删除一个不存在的用户")
        return {"code": 400, "msg": TEXT_USER_NOT_EXIST, "data": {}}


@app.get("/")
async def root():
    return {"code": 200, "msg": TEXT_INDEX, "data": {}}
