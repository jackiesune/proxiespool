import json
from utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count=0
#        attrs={}
        attrs['__CrawlFunc__']=[]
        print(type(attrs['__CrawlFunc__']))

        for k,v in attrs.items():
            if 'crawl_' in k:
                print(type(attrs['__CrawlFunc__']))
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)



class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies=[]
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理",proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=5):
        '''获取代理'''
        start_url='http://www.89ip.cn/index_{}.html'
 #       start_url='http://www.66ip.cn/areaindex_{}/1.html'
        urls=[start_url.format(page) for  page in range(1,page_count+1)]
        for url in urls:
            print("Crawling",url)
            html=get_page(url)
            if html:
                doc=pq(html)
                trs=doc('.layui-table tbody tr').items()
                print('找到一个网页')
                for tr in trs:

                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])



    


