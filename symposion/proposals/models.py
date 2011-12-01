import datetime

from django.db import models

from markitup.fields import MarkupField

from symposion.conference.models import PresentationKind, PresentationCategory


class Proposal(models.Model):
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters."
    )
    kind = models.ForeignKey(PresentationKind)
    category = models.ForeignKey(PresentationCategory)
    abstract = MarkupField(
        help_text = "Detailed description and outline. Will be made public if your talk is accepted. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    additional_notes = MarkupField(
        blank=True,
        help_text = "Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    extreme = models.BooleanField(
        default=False,
        help_text = "'Extreme' talks are advanced talks with little or no introductory material. See <a href='http://us.pycon.org/2012/speaker/extreme/' target='_blank'>http://us.pycon.org/2012/speaker/extreme/</a> for details."
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    def can_edit(self):
        return True
    
    @property
    def speaker_email(self):
        return self.speaker.email

    @property
    def number(self):
        return str(self.pk).zfill(3)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
