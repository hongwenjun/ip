import re, ipdb, ipaddress
db = ipdb.BaseStation("/app/qqwry.ipdb")
with open("/app/iplist.txt", "r") as f:
    data = f.read()

iplist = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data)
for ip in iplist:
   try:
      ipaddress.ip_address(ip).is_global
      city = db.find(ip, "CN")
      print(ip + " @" + city[0] + city[1] + city[2] + city[3])
   except:
      pass

# 统计日志中IP排名写到iplist.txt，批量查IP地址信息，最新日志100条
"""
docker logs ip 2>/dev/null \
  | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' \
  | sort | uniq -c| sort -nrk 1 | head -n 100 | tee iplist.txt

docker exec -it ip python3 ipinfo.py

docker logs ip 2>/dev/null | tail -100 

"""
