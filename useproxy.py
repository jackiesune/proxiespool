import requests

PROXY_POOL='http://0.0.0.0:5555/random'

def get_proxy():
    try:
        response=requests.get(url=PROXY_POOL)
        if response.status_code==200:
            return response.text
    except :
        return None





proxy=get_proxy()
proxies={
    "http":"http://"+proxy,
    "https":'https://'+proxy
}
s=requests.Session()
r=s.get('http://httpbin.org/get',proxies=proxies)
print(r.text)
