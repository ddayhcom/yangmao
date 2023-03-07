import time
import requests
import base64
import json
from datetime import datetime

cookie="" #账号cookie
#在	https://tly.sh/2301701  注册登录后  F12  随便刷新就可以抓到了 

token='free' #验证码token 每日限制5次  更错次数建议自行申请

#token在http://www.bhshare.cn/imgcode/gettoken/ 自行申请

def imgcode_online(imgurl):
    data = {
   
        'token': token,
        'type': 'online',
        'uri': imgurl
    }
    response = requests.post('http://www.bhshare.cn/imgcode/', data=data)
    print(response.text)
    result = json.loads(response.text)
    if result['code'] == 200:
        print(result['data'])
        return result['data']
    else:
        print(result['msg'])
        return 'error'


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()




def tly():
    signUrl="https://tly30.com/modules/index.php"
    hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','Cookie':cookie}

    res=requests.get(url=signUrl,headers=hearder).text
    signtime=getmidstring(res,'<p>上次签到时间：<code>','</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    t = int(time.time())

    if t-timeStamp>86400:
        print("距上次签到时间大于24小时啦,可签到")
        done=False
        while(done==False):
            #获取验证码图片
            captchaUrl="https://tly30.com/other/captcha.php"
            signurl="https://tly30.com/modules/_checkin.php?captcha="
            hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Cookie':cookie}
            res1=requests.get(url=captchaUrl,headers=hearder)
            base64_data = base64.b64encode(res1.content)
            oocr=imgcode_online('data:image/jpeg;base64,'+str(base64_data, 'utf-8'))
            res2=requests.get(url=signurl+oocr.upper(),headers=hearder).text
            print(res2)
            findresult=res2.find("流量")
            if findresult!=-1:
                done=True
            else:
                done=False
                print("未签到成功，沉睡3秒再来一次")
                time.sleep(3)
            
    else:
        print("还未到时间！",t-timeStamp)




    
 


def main_handler(event, context):
    tly()


if __name__ == '__main__':
    tly()

    




