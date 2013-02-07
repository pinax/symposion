from django.contrib import admin

from symposion_project.proposals.models import TalkProposal, TutorialProposal, PosterProposal


admin.site.register(TalkProposal)
admin.site.register(TutorialProposal)
admin.site.register(PosterProposal)
