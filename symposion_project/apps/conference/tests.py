import datetime
from datetime import timedelta
from django.test import TestCase

from . import models


class SessionKindTests(TestCase):
    def setUp(self):
        self.now = datetime.datetime.utcnow()
        self.future_conference = models.Conference(
            title="UeberCon",
            start_date=(self.now + timedelta(10)).date(),
            end_date=(self.now + timedelta(20)).date())
        self.future_conference.save()

    def tearDown(self):
        self.future_conference.delete()

    def test_sessionkind_explicitly_open_for_proposals(self):
        """
        A sessionkind is open for proposals if its conference is in the future
        and it is explicitly set to not being closed.
        """
        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            closed=False)
        kind.save()
        self.assertTrue(kind.accepts_proposals())

    def test_sessionkind_open_for_proposals_by_date(self):
        """
        A sessionkind is open for proposals if its conference is in the future
        and now is within the proposal submission time window.
        """
        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            start_date=(self.now - timedelta(2)),
            end_date=(self.now + timedelta(2)))
        kind.save()
        self.assertTrue(kind.accepts_proposals())

    def test_sessionkind_closed_for_proposals_by_conference(self):
        """
        A sessionkind is closed if its conference has already started.
        """
        conference = models.Conference(
            title="UeberCon",
            start_date=(self.now - timedelta(2)).date(),
            end_date=(self.now + timedelta(2)).date())
        conference.save()
        kind = models.SessionKind(
            name="Kind",
            conference=conference,
            closed=False)
        kind.save()
        self.assertFalse(kind.accepts_proposals())

    def test_sessionkind_explicitly_closed_for_proposals(self):
        """
        A sessionkind is closed if explicitly being marked as closed.
        """
        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            closed=True)
        kind.save()
        self.assertFalse(kind.accepts_proposals())

    def test_sessionkind_closed_for_proposals_by_date(self):
        """
        A sessionkind is closed for proposals if its submission time window
        has passed or is in the future.
        """
        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            start_date=self.now - timedelta(2),
            end_date=self.now - timedelta(1))
        kind.save()
        self.assertFalse(kind.accepts_proposals())

        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            start_date=self.now + timedelta(2),
            end_date=self.now + timedelta(3))
        kind.save()
        self.assertFalse(kind.accepts_proposals())

    def test_sessionkind_explicit_before_implicit(self):
        """
        If the conference is in the future, the "closed" flag on sessionkinds
        overrides any date settings.
        """
        kind = models.SessionKind(
            name="Kind",
            conference=self.future_conference,
            start_date=self.now - timedelta(2),
            end_date=self.now + timedelta(2),
            closed=True)
        kind.save()
        self.assertFalse(kind.accepts_proposals())

    def test_sessionkind_valid_start(self):
        """
        If there are start and end defined, end have to be after start.
        """
        kind = models.SessionKind(
            name="Kind",
            slug="kind",
            conference=self.future_conference,
            start_date=self.now - timedelta(2),
            end_date=self.now + timedelta(2),
            closed=None)
        kind.full_clean()
        kind.start_date = self.now + timedelta(2)
        kind.end_date = self.now
        try:
            kind.full_clean()
            self.fail()
        except Exception, _:
            pass
