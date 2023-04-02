# import socket
import requests
import re
import time

user = "你的账户"
password = "你的密码"

# 通过 socket 获取 baidu.com 的 IP 地址
# ip_address = socket.gethostbyname('baidu.com')
ip_address = "100.125.0.1"

while True:

    # 输出 IP 地址
    print('baidu.com 的 IP 地址为：', ip_address)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        # 使用 Session 对象
        session = requests.Session()

        # 访问 IP 地址
        response = session.get(f'http://{ip_address}', headers=headers, allow_redirects=False)

        # 获取重定向的 URL
        if response.status_code == 302:
            redirect_url = response.headers['Location']
            print(f"重定向的网址: {redirect_url}")

            # 使用正则表达式提取 userip 和 basip
            userip_match = re.search(r'userip=([\d.]+)', redirect_url)
            basip_match = re.search(r'basip=([\d.]+)', redirect_url)
            ip_match = re.search(r'http://([\d.]+):\d+', redirect_url)

            if userip_match and basip_match and ip_match:
                userip = userip_match.group(1)
                basip = basip_match.group(1)
                redirect_ip = ip_match.group(1)
                print(f"userip: {userip}, basip: {basip}, redirect_ip: {redirect_ip}")

                # 生成新的 URL
                new_url = f'http://{redirect_ip}:7119/portal.wlan?wlanacname=&wlanacip={basip}&wlanuserip={userip}&ssid=edu'
                print(f"新的网址: {new_url}")

                # 访问新的 URL
                new_response = session.get(new_url, headers=headers)
                if new_response.status_code == 200:
                    # 从响应中提取 portalLogin
                    portal_login_match = re.search(r'<input type="hidden" name="portalLogin"  value = "([\w\d]+)"',
                                                   new_response.text)
                    if portal_login_match:
                        portal_login = portal_login_match.group(1)
                        print(f"portalLogin: {portal_login}")

                        # 构建 POST 数据
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

                        # 生成 13 位时间戳
                        timestamp = int(time.time() * 1000)
                        post_url = f'http://{redirect_ip}:7119/portalLogin.wlan?{timestamp}'

                        # 发送 POST 请求
                        post_response = session.post(post_url, headers=headers, data=data)
                        print("发送 POST 请求完成")
                        print(post_url)
                        print(f"响应状态码: {post_response.status_code}")

                        # 强制顶号
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

                        # 发送 POST 请求
                        post_response = session.post(post_url, headers=headers, data=data)
                        print("发送 POST 请求完成")
                        print(post_url)
                        print(f"响应状态码: {post_response.status_code}")

                        # # 下线
                        # data = {
                        #     "wlanAcName": "",
                        #     "wlanAcIp": basip,
                        #     "wlanUserIp": userip,
                        #     "ssid": "edu",
                        #     "userName": user,
                        #     "logonsessid": "",
                        #     "encryUser": "",
                        #     "booktime": "",
                        #     "validperiod": "",
                        #     "passType": "1",
                        #     "cookies": "",
                        #     "isLocalUser": ""
                        # }
                        #
                        # time.sleep(10)
                        #
                        # # 生成 13 位时间戳
                        # timestamp = int(time.time() * 1000)
                        # post_url = f'http://{redirect_ip}:7119/portalLogout.wlan?{timestamp}&isCloseWindow=N'
                        #
                        # # 发送 POST 请求
                        # post_response = session.post(post_url, headers=headers, data=data)
                        # print("发送 POST 请求完成")
                        # print(post_url)
                        # print(f"响应状态码: {post_response.status_code}")
                    else:
                        print("未能从新的网址中提取 portalLogin")
                else:
                    print(f"访问 {new_url} 未能获取到响应数据")
            else:
                print("未能从重定向网址中提取 userip, basip 或 redirect_ip")
        else:
            print(f"访问 {ip_address} 未能获取到重定向信息")
    except Exception as e:
        print(f"发生错误：{e}")

    time.sleep(300)
