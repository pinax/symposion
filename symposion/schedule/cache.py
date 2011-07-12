from django.conf import settings

try:
    import redis
except ImportError:
    redis = None


if redis:
    db = redis.Redis(**settings.REDIS_PARAMS)
    try:
        db.ping()
    except redis.ConnectionError:
        db = None
else:
    db = None


prefix = "pycon2011-schedule"


def cache_key():
    return prefix


def cache_key_user(user):
    return "%s-%d" % (prefix, user.id)
