from redis import Redis

redis_cli = Redis(host='localhost', port=6379, decode_responses=True)