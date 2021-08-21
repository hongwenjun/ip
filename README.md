## ip:  Python WebAPI

### 演示网址  https://262235.xyz/ip/

### 本WebAPI支持IP城市定位和域名查IP定位，同时支持命令行查询

![](https://262235.xyz/usr/uploads/2021/08/3947416904.png)

## 安装部署简易命令
```
git clone https://github.com/hongwenjun/ip.git
pip3  install Flask  ipip-ipdb
cd ip
wget https://cdn.jsdelivr.net/npm/qqwry.ipdb/qqwry.ipdb
flask run --host=0.0.0.0
```

## Docker容器傻瓜部署
- 如果要挂载 `/app` 目录，宿主机先准备好文件
```
docker run -d -p 80:5000 --restart=always --name ip hongwenjun/ip
```

### 搭建WebAPI参考文章
[Python网络开发简单的IP城市定位WebAPI](https://262235.xyz/index.php/archives/342/)

