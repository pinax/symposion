from __future__ import with_statement

from django import template

from symposion.schedule.cache import db, cache_key, cache_key_user


register = template.Library()


class ScheduleCacheNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        nodelist = parser.parse(("endschedule_cache",))
        parser.delete_first_token()
        return cls(nodelist)
    
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        if db:
            user = context["user"]
            key = cache_key_user(user) if user.is_authenticated() else cache_key()
            output = db.get(key)
            if output is None:
                with db.lock("%s-lock" % key):
                    # check for cached data if we lost lock acquisition and
                    # if nothing was returned we can be sure we own the lock
                    output = db.get(key)
                    if output is None:
                        output = self.nodelist.render(context)
                        db.set(key, output)
        else:
            output = self.nodelist.render(context)
        return output


@register.tag
def schedule_cache(parser, token):
    return ScheduleCacheNode.handle_token(parser, token)
