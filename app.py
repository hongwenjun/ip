import ipdb, ipaddress, requests, json
from flask import Flask, request, render_template, jsonify
from socket import gethostbyname

db = ipdb.BaseStation("qqwry.ipdb")
app = Flask(__name__)

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

def ip2bdgps(ip):
    url = 'https://api.map.baidu.com/location/ip?ak=iUGOVyqGFo4QOP6QhTuZPF1P6FV5GB7p&coor=bd09ll&ip=' + ip
    r = requests.get(url)
    json_str = r.text
    data = json.loads(json_str)

    if data['status'] != 0 :
        return  (116.39564504, 39.92998578 , data['status'])    # 查不到返回 北京 x,y
    else:
        x = data['content']['point']['x']
        y = data['content']['point']['y']
    return  (x, y, data['status'], data)

@app.route("/")
def hello():
    ip = getip()
    if is_Mozilla():
        return ip + render_template('hello.html', ip=ip) + "\n\n" + request.headers["User-Agent"]
    else:
        return ip

@app.route("/ip/maps/")
def maps():
    ip = getip()
    bdgps = ip2bdgps(ip)
    return  render_template('maps.html',  bdgps=bdgps)

@app.route("/ip/")
@app.route("/ip/<ipaddr>")
def show_ip(ipaddr=None):
    # ip 地址为空获得浏览器客户端IP
    if ipaddr is None:
        ip = getip()
        ipaddr = iplocated(ip)
        if is_Mozilla():
            return  render_template('hello.html',  ip=ip, ipaddr=ipaddr, city=getcity(ip))
        else:
            return ip
    else:
        ip = ipaddr

    # ip地址 从纯真IP数据库 搜索城市定位
    try:
        ipaddress.ip_address(ip).is_global
        ipaddr = iplocated(ip)
    except:
        try:
            ip = gethostbyname(ip)     # 域名反解析得到的IP
            ipaddr = iplocated(ip)
        except Exception as e:
            print(e)

    return ipaddr




if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

# export FLASK_ENV=development   # 调试模式: 修改代码不用重启服务
# flask run --host=0.0.0.0       # 监听所有公开的 IP


