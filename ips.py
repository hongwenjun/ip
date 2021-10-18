import ipdb, ipaddress, requests, re, json
from flask import Flask, request
from socket import gethostbyname

from ctypes import *
# GPS火星坐标互转
# from china_shift import *

class Location(Structure):
    _fields_ = [
        ('lon', c_double),
        ('lat', c_double)]

db = ipdb.BaseStation("qqwry.ipdb")

def iplocated(ip):
    city = db.find(ip, "CN")
    return ip + " @" + city[0] + city[1] + city[2] + city[3] + "\n"

def getcity(ip):
    city = db.find(ip, "CN")
    return  city[2] + '市'

def getip():
    ip = request.remote_addr
    try:
        _ip = request.headers["X-Real-IP"]
        if _ip is not None:
            ip = _ip
    except Exception as e:
        print(e)
    return ip

def is_Mozilla():
    # Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
    ua = request.headers["User-Agent"]
    if (ua.find("Mozilla") != -1):
        return True
    else:
        return False

## 百度免费的 IP 普通定位 API 接口 
def ip2bdgps(ip):
    url = 'https://api.map.baidu.com/location/ip?ak=>>>百度AK码<<<&coor=bd09ll&ip=' + ip
    try:
        r = requests.get(url)
        data = r.json()
    except :
        return

    if data['status'] != 0 :
        return  (116.39564504, 39.92998578 , data['status'])    # 查不到返回 北京 x,y
    else:
        x = data['content']['point']['x']
        y = data['content']['point']['y']
    return  (x, y, data['status'], data)

## 免费试用500次,  1元能使用1万次 IP定位 API 接口   https://market.aliyun.com/products/57002002/cmapi00035184.html
def ip2gdgps(ip):
    url = 'http://ips.market.alicloudapi.com/iplocaltion?ip=' + ip
    headers = {"Authorization":"APPCODE <<<APPCODE>>>" ,"Content-Type":"application/json; charset=utf-8" }
    try:
        r = requests.get(url=url , headers=headers)
        data = r.json()
    except :
        return
    # print(data)
    if data['code'] != 100:
        return  (116.39564504, 39.92998578 , data['code'])    # 查不到返回 北京 x,y
    elif data['message'] == "success":
        x = data['result']['lng']
        y = data['result']['lat']
        loc = Location(lon = float(x), lat = float(y))
#       loc = shift.transformFromWGSToGCJ(loc)
        # loc = shift.bd_encrypt(loc)
        return  (loc.lon, loc.lat, data['code'], data)

def select_ips(ips_text):
    ret =''
    iplist = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ips_text)
    for ip in iplist:
        try:
            one = iplocated(ip)
            ret+=one
        except:
            pass
    return ret