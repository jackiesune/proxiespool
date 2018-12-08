from operate_pr import RedisClient
from getproxyfromnet import Crawler

POOL_UPPER_THRESHOLD=10000

class Getter():
    def __init__(self):
        self.redis=RedisClient()
        self.crawler=Crawler()


    def is_over_threshold(self):
        '''判断是否超过代理最大数量'''
        if self.redis.count() >=POOL_UPPER_THRESHOLD:
            return True

        else:return False

    def run(self):
        print("开始获取proxy")
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback=self.crawler.__CrawlFunc__[callback_label]
                proxies=self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)




