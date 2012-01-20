from django import template

from symposion.sponsors.models import Sponsor


register = template.Library()


class SponsorsNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 4:
            raise template.TemplateSyntaxError("%r takes exactly three arguments "
                "(second argument must be 'as')" % bits[0])
        if bits[2] != "as":
            raise template.TemplateSyntaxError("Second argument to %r must be "
                "'as'" % bits[0])
        return cls(bits[1], bits[3])
    
    def __init__(self, level, context_var):
        self.level = template.Variable(level)
        self.context_var = context_var
    
    def render(self, context):
        level = self.level.resolve(context)
        queryset = Sponsor.objects.filter(
            level__name__iexact = level,
            active = True
            ).order_by(
                "added"
            )
        context[self.context_var] = queryset
        return u""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors "gold" as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)
