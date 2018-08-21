"""
展示redis解析的脚本
"""
import redis

if __name__ == '__main__':
    r = redis.Redis(port=6380)
    r.set('a', 1, 3000)
    r.get('a')
    r.lpush('list', *range(10))
    r.lrange('list', 0, -1)
