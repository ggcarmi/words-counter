import redis as redis

import os

redis_host = os.getenv("DATABASE_URI")
db = redis.Redis(host=redis_host, port=6379, db=0)



