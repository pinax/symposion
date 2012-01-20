from django import template

from symposion.sponsors_pro.models import Sponsor


register = template.Library()


class SponsorsNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        section = "all"
        if len(bits) != 3 and len(bits) != 4:
            raise template.TemplateSyntaxError("%r takes two to three arguments "
                "(second to last argument must be 'as')" % bits[0])
        if bits[-2] != "as":
            raise template.TemplateSyntaxError("Second to last argument to %r must be "
                "'as'" % bits[0])
        if len(bits) == 4:
            section = bits[1]
        return cls(bits[-1], section)
    
    def __init__(self, context_var, section):
        self.section = section
        self.context_var = context_var
    
    def render(self, context):
        queryset = Sponsor.objects.active()
        queryset = queryset.select_related("level", "sponsor_logo")
        if self.section == "header":
            queryset = queryset.filter(level__in=[1])
        if self.section == "scroll":
            queryset = queryset.filter(level__in=[2, 3])
        if self.section == "footer":
            queryset = queryset.filter(level__in=[4, 10])
        if self.section == "jobs":
            queryset = queryset.filter(level__in=[1, 2, 3, 4, 7])
        context[self.context_var] = queryset
        return u""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors [header, scroll, footer, all] as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)
