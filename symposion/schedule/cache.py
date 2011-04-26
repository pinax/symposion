from django.conf import settings

import redis


db = redis.Redis(**settings.REDIS_PARAMS)
try:
    db.ping()
except redis.ConnectionError:
    db = None


prefix = "pycon2011-schedule"


def cache_key():
    return prefix


def cache_key_user(user):
    return "%s-%d" % (prefix, user.id)
