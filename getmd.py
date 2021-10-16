import requests, html2text, re

# 请求头，模拟浏览器UA
headers = {'User-Agent': ' '.join(['Mozilla/5.0 (Windows NT 10.0; Win64; x64; ServiceUI 14)',
            'AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/70.0.3538.102', 'Safari/537.36','Edge/18.18363']) }

def url_to_markdown(url):
    # 发送请求
    r = requests.get(url=url, headers=headers)
    # html 转换 markdown
    html = r.text
    text = html2text.html2text(html)
    return text

def pull_urls(urls_list):
    texts =''
    for url in urls_list:
      texts += url_to_markdown(url)
    return texts

# 正则搜索得到网址URL
def get_url(line):
    reg_https = r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    url = re.search(reg_https, line)
    return url

# 检查获得多行URL
def check_urls(urls):
    ret = []
    lines = urls.split('\n')
    for line in lines:
        url = get_url(line)
        if url is not None:
            ret.append(url[0])
    ret = list(set(ret))
    return ret

def urls_lines(urls_list):
    str = '\n'.join(urls_list)
    return str


import base64 , hashlib, time
# 构建 PASSKEY
def make_passkey(str=''):
    s = time.strftime("%Y%m%d-%H", time.localtime()) + str
    b = s.encode("utf-8")
    m = hashlib.sha256()
    m.update(b)
    passkey = base64.b64encode(m.digest()).decode("utf-8")[8:16]
    return passkey