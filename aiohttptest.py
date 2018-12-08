from operate_pr import RedisClient
import aiohttp
import asyncio
import sys
import time
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
#from proxypool.setting import *



VALID_STATUS_CODES=[200]
TEST_URL='https://www.baidu.com'
BATCH_TEST_SIZE=100


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()




    async def test_single_proxy(self,proxy):
        '''执行单个代理测试'''
        print(type(proxy))
        conn=aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy=proxy.decode('utf-8')
                real_proxy='http://'+proxy
                print('正在执行测试',proxy)

                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('设置'+str(proxy))
                    else:
                        self.redis.decrease(proxy)
                        print('响应吗不合法',proxy)
                print('测试了',proxy)
            except (ClientError,ClientConnectorError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                print('请求失败',proxy)

    def run(self):
        '''主函数'''

        print('测试开始了')

        try:
            proxies=self.redis.all()
            loop=asyncio.get_event_loop()
            '''同时进行测试'''
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies=proxies[i:i+BATCH_TEST_SIZE]
                tasks=[self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(4)
        except Exception as e:
            print('出现错误',e.args)
