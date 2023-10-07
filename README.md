## ip: Python Flask WebAPI && Bootstrap Theme

##【Docker 学习 WebAPI 之 IP 城市定位 容器傻瓜部署】 [B站视频](https://www.bilibili.com/video/BV1NC4y157Zb)
### https://www.bilibili.com/video/BV1NC4y157Zb

### 演示网址1  https://262235.xyz/ip/
### 演示网址2  https://lyvba.com/ip/

### 本WebAPI支持IP城市定位和域名查IP定位，同时支持命令行查询

![](https://262235.xyz/usr/uploads/2021/10/4246023144.png)

## 安装部署简易命令
```
git clone https://github.com/hongwenjun/ip.git
pip3  install Flask  ipip-ipdb  html2text
cd ip
wget https://cdn.jsdelivr.net/npm/qqwry.ipdb/qqwry.ipdb
flask run --host=0.0.0.0
```

## Docker容器傻瓜部署
- 如果要挂载 `/app` 目录，宿主机先准备好文件
```
docker run -d -p 80:5000 --restart=always --name ip hongwenjun/ip

# 使用另一个 python3 镜像挂载
docker run -d -p 80:80  -v /root/ip:/app \
  --restart=always --name python3   \
  hongwenjun/python3   python3 -m   app
```

  * [github源码](https://github.com/hongwenjun/ip)
  * [docker镜像](https://hub.docker.com/r/hongwenjun/ip)
  * [搭建WebAPI参考文章](https://262235.xyz/index.php/search/webapi/)
  * 在线工具箱
    * [Bootstrap theme](https://262235.xyz/bs/)
    * [编程中文文档](https://www.262235.xyz/index.php/246.html)
    * [Linux 命令列表](https://262235.xyz/linux-command/)
    * [IP定位和地图](https://262235.xyz/ip/)
    * [批量IP查询](https://262235.xyz/ips/)
    * [批量网址转Markdown](https://262235.xyz/getmd/)
    * [Markdown编辑器](https://tool.lu/markdown/)

[Pytyhon 使用百度地图API 进行 IP普通定位和地图显示](https://www.262235.xyz/index.php/archives/375/)

演示网址: https://www.262235.xyz/ip/maps/

### GPS定位百度的太拉，推荐购买:  
- 免费试用500次, 1元能使用1万次 IP定位 API 接口   https://market.aliyun.com/products/57002002/cmapi00035184.html
- 高德 IP定位  0元／100000次    https://market.aliyun.com/products/57002002/cmapi018957.html
- `app.py` 中请更换你自己的 API
```
def ip2gdgps(ip):
    url = 'http://iploc.market.alicloudapi.com/v3/ip=' + ip
    headers = {"Authorization":"APPCODE  <<<IP定位APPCODE>>>" ,"Content-Type":"application/json; charset=utf-8" }
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
        return  (x, y, data['code'], data)
```
