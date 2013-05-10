from django.db import models

from symposion.proposals.models import ProposalBase


class Proposal(ProposalBase):
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    
    recording_release = models.BooleanField(
        default=True,
        help_text=(
            'By submitting your talk proposal, you agree to license the '
            'presentation video and audio under the '
            '<a href="http://creativecommons.org/licenses/by-sa/2.5/ca/">Creative Commons Attribution-ShareAlike <img src="https://i.creativecommons.org/l/by-sa/2.5/ca/88x31.png" /></a> '
            'license (like most of '
            '<a href="http://en.wikipedia.org/wiki/Wikipedia:Copyrights">Wikipedia</a>). '
            'If you do not agree to this, please uncheck this box.')
    )
    
    class Meta:
        abstract = True


class TalkProposal(Proposal):
    class Meta:
        verbose_name = "talk proposal"


class TutorialProposal(Proposal):
    class Meta:
        verbose_name = "tutorial proposal"


class LightningProposal(Proposal):
    class Meta:
        verbose_name = "lightning proposal"


class PosterProposal(Proposal):
    class Meta:
        verbose_name = "poster proposal"
