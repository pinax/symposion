from django.db import models


class SponsorManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(active=True).order_by("level")
    
    def with_weblogo(self):
        queryset = self.raw("""
        SELECT DISTINCT
            "sponsorship_sponsor"."id",
            "sponsorship_sponsor"."applicant_id",
            "sponsorship_sponsor"."name",
            "sponsorship_sponsor"."external_url",
            "sponsorship_sponsor"."annotation",
            "sponsorship_sponsor"."contact_name",
            "sponsorship_sponsor"."contact_email",
            "sponsorship_sponsor"."level_id",
            "sponsorship_sponsor"."added",
            "sponsorship_sponsor"."active",
            "sponsorship_sponsorlevel"."order"
        FROM
            "sponsorship_sponsor"
            INNER JOIN
                "sponsorship_sponsorbenefit" ON ("sponsorship_sponsor"."id" = "sponsorship_sponsorbenefit"."sponsor_id")
            INNER JOIN
                "sponsorship_benefit" ON ("sponsorship_sponsorbenefit"."benefit_id" = "sponsorship_benefit"."id")
            LEFT OUTER JOIN
                "sponsorship_sponsorlevel" ON ("sponsorship_sponsor"."level_id" = "sponsorship_sponsorlevel"."id")
        WHERE (
            "sponsorship_sponsor"."active" = 't' AND
            "sponsorship_benefit"."type" = 'weblogo' AND
            "sponsorship_sponsorbenefit"."upload" != ''
        )
        ORDER BY "sponsorship_sponsorlevel"."order" ASC, "sponsorship_sponsor"."added" ASC
        """)
        return queryset
