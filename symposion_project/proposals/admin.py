from django.contrib import admin

from symposion_project.proposals.models import TalkProposal, TutorialProposal, PosterProposal, LightningProposal


admin.site.register(TalkProposal)
admin.site.register(LightningProposal)
admin.site.register(TutorialProposal)
admin.site.register(PosterProposal)
