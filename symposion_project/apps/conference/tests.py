import datetime
from datetime import timedelta
from django.test import TestCase

from . import models


class SessionKindTests(TestCase):
    def setUp(self):
        self.now = datetime.datetime.utcnow()
        self.conference = models.Conference(
            title="UeberCon",
            start_date=self.now - timedelta(10),
            end_date=self.now + timedelta(10))
        self.conference.save()

    def tearDown(self):
        self.conference.delete()
        pass

    def test_open_sessionkind(self):
        kind = models.SessionKind(
            name="Kind",
            conference=self.conference,
            closed=False)
        kind.save()
        self.assertTrue(kind.accepts_proposals())

        kind = models.SessionKind(
            name="Kind",
            conference=self.conference,
            closed=None,
            start_date=self.now - timedelta(1),
            end_date=self.now + timedelta(1))
        kind.save()
        self.assertTrue(kind.accepts_proposals())
