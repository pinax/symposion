from django.contrib import admin

from symposion_project.proposals.models import ProposalCategory, TalkProposal, TutorialProposal, PosterProposal

admin.site.register(ProposalCategory,
    prepopulated_fields = {"slug": ("name",)},
)
admin.site.register(TalkProposal)
admin.site.register(TutorialProposal)
admin.site.register(PosterProposal)
