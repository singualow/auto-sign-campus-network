# ps | grep sign
# nohup python -u sign.py > /dev/null 2>&1 &

import requests
import time
import socket
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

if(os.path.isfile("log")):
    os.remove("log")


def setup_logger():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = 'log'
    max_log_size = 3 * 1024 * 1024
    backup_count = 2
    handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
    handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def current_time_formatted():
    now = datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def get_local_ip():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('223.5.5.5', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip


def test(session, host):
    try:
        response = session.get(f'http://{host}', timeout=2)
        return response.status_code == 404
    except Exception:
        return False


logger = setup_logger()

user = "你的账号"
password = "你的密码"
basip = "211.137.223.246"
redirect_ip = "111.26.29.8"
portal_login = "2849ff12f0aa4b30989f500d689d7742"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
session = requests.Session()

while True:
    if not test(session, "223.5.5.5"):
        try:
            userip = get_local_ip()
            data = {
                "wlanAcName": "",
                "wlanAcIp": basip,
                "wlanUserIp": userip,
                "ssid": "edu",
                "portalLogin": portal_login,
                "passType": "1",
                "userName": user,
                "userPwd": password
            }
            timestamp = int(time.time() * 1000)
            post_url = f'http://{redirect_ip}:7119/portalLogin.wlan?{timestamp}'
            session.post(post_url, headers=headers, data=data)
            data = {
                "wlanAcName": "",
                "wlanAcIp": basip,
                "wlanUserIp": userip,
                "ssid": "edu",
                "passType": "1",
                "userName": user,
                "userPwd": password,
                "autoLogin": "false",
                "onlineInfo": ""
            }
            post_url = f'http://{redirect_ip}:7119/portalForceLogin.wlan'
            session.post(post_url, headers=headers, data=data)
            logger.info("连接成功：自动连接成功")
        except Exception as e:
            logger.error("发生错误：未连接校园网")
            time.sleep(1)
    else:
        # logger.info("自动检测：目前连接正常")
        time.sleep(2)
