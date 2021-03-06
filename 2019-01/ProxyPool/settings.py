REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

INITIAL_SCORE = 10
MAX_SCORE = 100
MIN_SCORE = 0

POOL_UPPER_THRESHOLD = 1000

TEST_URL = 'https://mp.weixin.qq.com'
VALID_STATUS_CODE = [200, 302]
BATCH_TEST_SIZE = 5

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLE = True
GETTER_ENABLE = True

API_ENABLE = True
API_HOST = '127.0.0.1'
API_PORT = '5555'