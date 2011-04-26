from django import template

from sponsors.models import Sponsor


register = template.Library()


class SponsorsNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 3:
            raise template.TemplateSyntaxError("%r takes exactly two arguments "
                "(first argument must be 'as')" % bits[0])
        if bits[1] != "as":
            raise template.TemplateSyntaxError("First argument to %r must be "
                "'as'" % bits[0])
        return cls(bits[2])
    
    def __init__(self, context_var):
        self.context_var = context_var
    
    def render(self, context):
        queryset = Sponsor.objects.filter(
            active = True
            ).order_by("level", "added")
        context[self.context_var] = queryset
        return u""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)
