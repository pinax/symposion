from django.db import models

from symposion.proposals.models import ProposalBase


class PyConProposalCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "PyCon proposal category"
        verbose_name_plural = "PyCon proposal categories"


class PyConProposal(ProposalBase):
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    category = models.ForeignKey(PyConProposalCategory)
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    
    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2013/speaking/recording/' target='_blank'>PyCon 2013 Recording Release</a> for details."
    )
    
    class Meta:
        abstract = True


class PyConTalkProposal(PyConProposal):
    
    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
    ]
    
    extreme = models.BooleanField(
        default=False,
        help_text="'Extreme' talks are advanced talks with little or no introductory material. See <a href='http://us.pycon.org/2013/speaker/extreme/' target='_blank'>Extreme Talks</a> for details."
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)
    
    class Meta:
        verbose_name = "PyCon talk proposal"


class PyConTutorialProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon tutorial proposal"


class PyConPosterProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon poster proposal"
