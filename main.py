import requests
import time
import playsound

time_interval = 30 # 每幾秒檢查一次是否有題目
target_url = '' # 題目頁面，例如：https://irs.zuvio.com.tw/student5/irs/clickers/1293880
payload = {
    'email': '',  # 填入你的 Zuvio 帳號
    'password': '', # 填入你的 Zuvio 密碼
    'current_language': 'zh_TW', 
    'back_url': ''
}
login_url = 'https://irs.zuvio.com.tw/irs/login'
submit_url = 'https://irs.zuvio.com.tw/irs/submitLogin'

chk = False
defalut_response = ''
while True:
    with requests.Session() as session:
        response = session.get(login_url)
        if response.status_code == 200:
            if(chk == False): print('Get session success!')
            login_response = session.post(submit_url, data=payload)
            if login_response.status_code == 200:
                if(chk == False): print('Login success!')
                target_response = session.get(target_url)
                if target_response.status_code == 200:
                    if(chk == False): print('Get target page success!')
                    target_response.encoding = 'utf-8'
                    if chk == False:
                        defalut_response = target_response.text
                        chk = True
                    elif defalut_response != target_response.text:
                        print('There is a new Quiz!')
                        playsound.playsound('ring.mp3') # 可以更改提醒聲
                    else:
                        print('\rNo new Quiz', end='')
                else:
                    print(f'Get target page failed, Error code：{target_response.status_code}')
            else:
                print(f'Login failed, Error code：{login_response.status_code}')
        else:
            print(f'Get session failed, Error code：{response.status_code}')
    time.sleep(time_interval)
