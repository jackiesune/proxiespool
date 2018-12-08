MAX_SCORE=90
MIN_SCORE=0
INITIAL_SCORE=10
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD='foobared'
REDIS_KEY='proxies'


import redis
from random import choice
from error import PoolEmptyError




class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """初始化"""

        self.db=redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
    
    def add(self,proxy,score=INITIAL_SCORE):
        '''添加代理 设置分数'''
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        '''获得随机代理'''
        result=self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)+'max'
        else:
            result=self.db.zrevrange(REDIS_KEY,70,100)
            if len(result):
                return choice(result)
            else:raise PoolEmptyError

    def decrease(self,proxy):
        '''代理减分，直至删除'''

        score=self.db.zscore(REDIS_KEY,proxy)
        if score and score >MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        '''判断是否存在'''

        return not self.db.zscore(REDIS_KEY,proxy)==None

    def max(self,proxy):
        '''将代理设置为MAX_SCORE'''
        print('代理',proxy,'可用设置为',MAX_SCORE)
        return self.db.zadd(REIDS_KEY,MAX_SCORE,proxy)

    def count(self):
        '''获取数量'''

        return self.db.zcard(REDIS_KEY)

    
    def all(self):
        '''获取全部代理'''

        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)





