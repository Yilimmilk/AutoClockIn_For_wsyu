## 环境：

python3.6.11 , mysql5.7

## 克隆项目

在你需要的目录下执行

```
git clone https://github.com/Yilimmilk/AutoClockIn_For_wsyu.git
```

## 安装依赖

进入项目文件夹

使用`pip`安装所需模块

```
pip install -r requirements.txt
```

## 修改配置

所有配置均可在`ConfigConst.py`文件中修改。

我都写了备注，应该很清晰明了。

## 运行程序

使用uvicorn启动（推荐），若使用此方法启动，请在startup.py中修改相关参数。
```
python startup.py
```
或使用fastapi原版启动
```
python main.py
```
## 接口使用

### 一键打卡
```
/clock_in
```

请求代码示例：
```python
import requests

# POST
params = {
    'username': 'xxxxx',    #一般为学号
    'password': 'xxxxx'     #一般为姓名
}
requests.post('http://ip:port/clock_in', params=params)
```
请求数据格式

|     请求方式     |   参数   |  说明  | 是否必须 |
|:------------:| :------: | :----: | :------: |
|   **POST**   | username |  账号  |    是    |
|              | password |  密码  |    是    |


**在学校的疫情防控系统里面，username为学号，password为姓名即可登陆**