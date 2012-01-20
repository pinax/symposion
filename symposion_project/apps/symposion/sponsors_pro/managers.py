from django.db import models


class SponsorManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(active=True).order_by("level")
    
    def with_weblogo(self):
        queryset = self.raw("""
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
        return queryset
