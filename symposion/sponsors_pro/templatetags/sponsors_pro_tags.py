from django import template

from symposion.sponsors_pro.models import Sponsor


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
        queryset = Sponsor.objects.raw("""
        SELECT DISTINCT
            "sponsors_pro_sponsor"."id",
            "sponsors_pro_sponsor"."applicant_id",
            "sponsors_pro_sponsor"."name",
            "sponsors_pro_sponsor"."external_url",
            "sponsors_pro_sponsor"."annotation",
            "sponsors_pro_sponsor"."contact_name",
            "sponsors_pro_sponsor"."contact_email",
            "sponsors_pro_sponsor"."level_id",
            "sponsors_pro_sponsor"."added",
            "sponsors_pro_sponsor"."active",
            "sponsors_pro_sponsorlevel"."order"
        FROM
            "sponsors_pro_sponsor"
            INNER JOIN
                "sponsors_pro_sponsorbenefit" ON ("sponsors_pro_sponsor"."id" = "sponsors_pro_sponsorbenefit"."sponsor_id")
            INNER JOIN
                "sponsors_pro_benefit" ON ("sponsors_pro_sponsorbenefit"."benefit_id" = "sponsors_pro_benefit"."id")
            LEFT OUTER JOIN
                "sponsors_pro_sponsorlevel" ON ("sponsors_pro_sponsor"."level_id" = "sponsors_pro_sponsorlevel"."id")
        WHERE (
            "sponsors_pro_sponsor"."active" = 't' AND
            "sponsors_pro_benefit"."type" = 'weblogo' AND
            "sponsors_pro_sponsorbenefit"."upload" != ''
        )
        ORDER BY "sponsors_pro_sponsorlevel"."order" ASC, "sponsors_pro_sponsor"."added" ASC
        """)
        context[self.context_var] = queryset
        return u""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors as sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)
