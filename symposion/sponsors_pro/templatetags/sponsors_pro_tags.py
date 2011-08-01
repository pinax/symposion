from django import template

from symposion.sponsors_pro.models import Sponsor


register = template.Library()


class SponsorsNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token, web_only=True):
        bits = token.split_contents()
        if len(bits) != 3:
            raise template.TemplateSyntaxError("%r takes exactly two arguments "
                "(first argument must be 'as')" % bits[0])
        if bits[1] != "as":
            raise template.TemplateSyntaxError("First argument to %r must be "
                "'as'" % bits[0])
        return cls(bits[2], web_only)
    
    def __init__(self, context_var, web_only):
        self.web_only = web_only
        self.context_var = context_var
    
    def render(self, context):
        if self.web_only:
            queryset = Sponsor.objects.with_weblogo()
        else:
            queryset = Sponsor.objects.active()
        context[self.context_var] = queryset
        return u""


@register.tag
def web_sponsors(parser, token):
    """
    {% web_sponsors as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token, web_only=True)


@register.tag
def sponsors(parser, token):
    """
    {% sponsors as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)
