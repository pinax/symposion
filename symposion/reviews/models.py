# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from symposion.proposals.models import ProposalBase
from symposion.schedule.models import Presentation


class ProposalScoreExpression(object):

    def as_sql(self, qn, connection=None):
        sql = "((3 * plus_one + plus_zero) - (minus_zero + 3 * minus_one))"
        return sql, []

    def prepare_database_save(self, unused):
        return self


class Votes(object):
    PLUS_ONE = "+1"
    PLUS_ZERO = "+0"
    MINUS_ZERO = u"−0"
    MINUS_ONE = u"−1"

    CHOICES = [
        (PLUS_ONE, u"+1 — Good proposal and I will argue for it to be accepted."),
        (PLUS_ZERO, u"+0 — OK proposal, but I will not argue for it to be accepted."),
        (MINUS_ZERO, u"−0 — Weak proposal, but I will not argue strongly against acceptance."),
        (MINUS_ONE, u"−1 — Serious issues and I will argue to reject this proposal."),
    ]
VOTES = Votes()


class ReviewAssignment(models.Model):
    AUTO_ASSIGNED_INITIAL = 0
    OPT_IN = 1
    AUTO_ASSIGNED_LATER = 2

    NUM_REVIEWERS = 3

    ORIGIN_CHOICES = [
        (AUTO_ASSIGNED_INITIAL, "auto-assigned, initial"),
        (OPT_IN, "opted-in"),
        (AUTO_ASSIGNED_LATER, "auto-assigned, later"),
    ]

    proposal = models.ForeignKey(ProposalBase)
    user = models.ForeignKey(User)

    origin = models.IntegerField(choices=ORIGIN_CHOICES)

    assigned_at = models.DateTimeField(default=datetime.now)
    opted_out = models.BooleanField(default=False)

    @classmethod
    def create_assignments(cls, proposal, origin=AUTO_ASSIGNED_INITIAL):
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        reviewers = User.objects.exclude(
            pk__in=[
                speaker.user_id
                for speaker in speakers
                if speaker.user_id is not None
            ] + [
                assignment.user_id
                for assignment in ReviewAssignment.objects.filter(
                    proposal_id=proposal.id)]
        ).filter(
            groups__name="reviewers",
        ).filter(
            Q(reviewassignment__opted_out=False) | Q(reviewassignment=None)
        ).annotate(
            num_assignments=models.Count("reviewassignment")
        ).order_by(
            "num_assignments", "?",
        )
        num_assigned_reviewers = ReviewAssignment.objects.filter(
            proposal_id=proposal.id, opted_out=0).count()
        for reviewer in reviewers[:max(0, cls.NUM_REVIEWERS - num_assigned_reviewers)]:
            cls._default_manager.create(
                proposal=proposal,
                user=reviewer,
                origin=origin,
            )


class ProposalMessage(models.Model):
    proposal = models.ForeignKey(ProposalBase, related_name="messages")
    user = models.ForeignKey(User)

    message = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        ordering = ["submitted_at"]


class Review(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey(ProposalBase, related_name="reviews")
    user = models.ForeignKey(User)

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, blank=True, choices=VOTES.CHOICES)
    comment = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.now, editable=False)

    def save(self, **kwargs):
        if self.vote:
            vote, created = LatestVote.objects.get_or_create(
                proposal=self.proposal,
                user=self.user,
                defaults=dict(
                    vote=self.vote,
                    submitted_at=self.submitted_at,
                )
            )
            if not created:
                LatestVote.objects.filter(pk=vote.pk).update(vote=self.vote)
                self.proposal.result.update_vote(self.vote, previous=vote.vote)
            else:
                self.proposal.result.update_vote(self.vote)
        super(Review, self).save(**kwargs)

    def delete(self):
        model = self.__class__
        user_reviews = model._default_manager.filter(
            proposal=self.proposal,
            user=self.user,
        )
        try:
            # find the latest review
            latest = user_reviews.exclude(pk=self.pk).order_by("-submitted_at")[0]
        except IndexError:
            # did not find a latest which means this must be the only one.
            # treat it as a last, but delete the latest vote.
            self.proposal.result.update_vote(self.vote, removal=True)
            lv = LatestVote.objects.filter(proposal=self.proposal, user=self.user)
            lv.delete()
        else:
            # handle that we've found a latest vote
            # check if self is the lastest vote
            if self == latest:
                # self is the latest review; revert the latest vote to the
                # previous vote
                previous = user_reviews.filter(submitted_at__lt=self.submitted_at)\
                    .order_by("-submitted_at")[0]
                self.proposal.result.update_vote(self.vote, previous=previous.vote, removal=True)
                lv = LatestVote.objects.filter(proposal=self.proposal, user=self.user)
                lv.update(
                    vote=previous.vote,
                    submitted_at=previous.submitted_at,
                )
            else:
                # self is not the latest review so we just need to decrement
                # the comment count
                self.proposal.result.comment_count = models.F("comment_count") - 1
                self.proposal.result.save()
        # in all cases we need to delete the review; let's do it!
        super(Review, self).delete()

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]

    @property
    def section(self):
        return self.proposal.kind.section.slug


class LatestVote(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey(ProposalBase, related_name="votes")
    user = models.ForeignKey(User)

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, choices=VOTES.CHOICES)
    submitted_at = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        unique_together = [("proposal", "user")]

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]


class ProposalResult(models.Model):
    proposal = models.OneToOneField(ProposalBase, related_name="result")
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    comment_count = models.PositiveIntegerField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    plus_one = models.PositiveIntegerField(default=0)
    plus_zero = models.PositiveIntegerField(default=0)
    minus_zero = models.PositiveIntegerField(default=0)
    minus_one = models.PositiveIntegerField(default=0)
    accepted = models.NullBooleanField(choices=[
        (True, "accepted"),
        (False, "rejected"),
        (None, "undecided"),
    ], default=None)
    status = models.CharField(max_length=20, choices=[
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("undecided", "undecided"),
        ("standby", "standby"),
    ], default="undecided")

    @classmethod
    def full_calculate(cls):
        for proposal in ProposalBase.objects.all():
            result, created = cls._default_manager.get_or_create(proposal=proposal)
            result.comment_count = Review.objects.filter(proposal=proposal).count()
            result.vote_count = LatestVote.objects.filter(proposal=proposal).count()
            result.plus_one = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.PLUS_ONE
            ).count()
            result.plus_zero = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.PLUS_ZERO
            ).count()
            result.minus_zero = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.MINUS_ZERO
            ).count()
            result.minus_one = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.MINUS_ONE
            ).count()
            result.save()
            cls._default_manager.filter(pk=result.pk).update(score=ProposalScoreExpression())

    def update_vote(self, vote, previous=None, removal=False):
        mapping = {
            VOTES.PLUS_ONE: "plus_one",
            VOTES.PLUS_ZERO: "plus_zero",
            VOTES.MINUS_ZERO: "minus_zero",
            VOTES.MINUS_ONE: "minus_one",
        }
        if previous:
            if previous == vote:
                return
            if removal:
                setattr(self, mapping[previous], models.F(mapping[previous]) + 1)
            else:
                setattr(self, mapping[previous], models.F(mapping[previous]) - 1)
        else:
            if removal:
                self.vote_count = models.F("vote_count") - 1
            else:
                self.vote_count = models.F("vote_count") + 1
        if removal:
            setattr(self, mapping[vote], models.F(mapping[vote]) - 1)
            self.comment_count = models.F("comment_count") - 1
        else:
            setattr(self, mapping[vote], models.F(mapping[vote]) + 1)
            self.comment_count = models.F("comment_count") + 1
        self.save()
        model = self.__class__
        model._default_manager.filter(pk=self.pk).update(score=ProposalScoreExpression())


class Comment(models.Model):
    proposal = models.ForeignKey(ProposalBase, related_name="comments")
    commenter = models.ForeignKey(User)
    text = models.TextField()

    # Or perhaps more accurately, can the user see this comment.
    public = models.BooleanField(choices=[(True, "public"), (False, "private")], default=False)
    commented_at = models.DateTimeField(default=datetime.now)


class NotificationTemplate(models.Model):

    label = models.CharField(max_length=100)
    from_address = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()


class ResultNotification(models.Model):

    proposal = models.ForeignKey(ProposalBase, related_name="notifications")
    template = models.ForeignKey(NotificationTemplate, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=datetime.now)
    to_address = models.EmailField()
    from_address = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()

    @property
    def email_args(self):
        return (self.subject, self.body, self.from_address, [self.to_address])


def promote_proposal(proposal):
    if hasattr(proposal, "presentation") and proposal.presentation:
        # already promoted
        presentation = proposal.presentation
    else:
        presentation = Presentation(
            title=proposal.title,
            description=proposal.description,
            abstract=proposal.abstract,
            speaker=proposal.speaker,
            section=proposal.section,
            proposal_base=proposal,
        )
        presentation.save()
        for speaker in proposal.additional_speakers.all():
            presentation.additional_speakers.add(speaker)
            presentation.save()

    return presentation


def unpromote_proposal(proposal):
    if hasattr(proposal, "presentation") and proposal.presentation:
        proposal.presentation.delete()


def accepted_proposal(sender, instance=None, **kwargs):
    if instance is None:
        return
    if instance.status == "accepted":
        promote_proposal(instance.proposal)
    else:
        unpromote_proposal(instance.proposal)
post_save.connect(accepted_proposal, sender=ProposalResult)
