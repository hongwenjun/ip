from typing import Text
import ipdb, ipaddress, requests, re, json
from flask import Flask, request, render_template, jsonify
from socket import gethostbyname

app = Flask(__name__)
from ips import *
from getmd import *

@app.route("/")
def hello():
    ip = getip()
    ipaddr = iplocated(ip)
    if is_Mozilla():
        return  render_template('hello.html',  ip=ip, ipaddr=ipaddr, city=getcity(ip))
    else:
        return ip

@app.route("/ip/maps/")
def maps():
    ip = getip()
    # bdgps = ip2bdgps(ip)   #  百度地图 IP 定位 API 比较慢 ，换用 免费 高德定位
    bdgps = ip2gdgps(ip)
    return  render_template('maps.html',  bdgps=bdgps)

@app.route("/ip/bdmaps/")
def bdmaps():
    ip = getip()
    bdgps = ip2bdgps(ip)   #  百度地图 IP 定位 API 比较慢
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

@app.route("/ips/", methods=['POST', 'GET'])
def getips():
    if request.method == 'POST':
        ips_text = request.form['ips']
        ips = select_ips(ips_text)
        return render_template('ips.html', ips=ips)
    else:
        return render_template('ips.html')

@app.route("/getmd/", methods=['POST', 'GET'])
def getmd(): 
    if request.method == 'POST' and request.form['passkey'] == make_passkey('262235.xyz') : 
        urls = request.form['urls']
        urls_list = check_urls(urls)
        urls = urls_lines(urls_list)
        if len(urls_list) < 5 :
            texts = '测试 PASSKEY 一次只允许最多抓取5篇文章,当前数量:' + str(len(urls_list))
            texts += pull_urls(urls_list)
            return render_template('getmd.html', urls=urls, texts=texts, passkey=make_passkey('262235.xyz'))
        else:
            texts = '文章大于5: 测试 PASSKEY 一次只允许最多抓取5篇文章,当前数量:' + str(len(urls_list))
            return render_template('getmd.html', urls=urls, texts=texts, passkey=make_passkey('262235.xyz')) 
    else:
        if request.method == 'POST' and request.form['passkey'] == 'UUID-1234-5678-1234' : 
            urls = request.form['urls']
            urls_list = check_urls(urls)
            urls = urls_lines(urls_list)
            texts = '授权 PASSKEY 无限制，当前数量:' + str(len(urls_list))
            texts += pull_urls(urls_list)
            return render_template('getmd.html', urls=urls, texts=texts)
        pass
    return render_template('getmd.html', passkey=make_passkey('262235.xyz'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0') 
    app.run(host='0.0.0.0', debug=True, port=80) 

# export FLASK_ENV=development   # 调试模式: 修改代码不用重启服务
# flask run --host=0.0.0.0       # 监听所有公开的 IP
