from django.core.urlresolvers import reverse
from django.test import TestCase

from django.contrib.auth.models import User, Group

from symposion.proposals.models import Proposal
from symposion.reviews.models import Review, ReviewAssignment


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args):
        self.testcase.client.logout()


class ReviewTests(TestCase):
    fixtures = ["proposals"]
    
    def get(self, url_name, *args, **kwargs):
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))
    
    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data")
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)
    
    def login(self, user, password):
        return login(self, user, password)
    
    def test_detail_perms(self):
        guidos_proposal = Proposal.objects.all()[0]
        response = self.get("review_detail", pk=guidos_proposal.pk)
        
        # Not logged in
        self.assertEqual(response.status_code, 302)
        
        with self.login("guido", "pythonisawesome"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Guido can see his own proposal.
            self.assertEqual(response.status_code, 200)
        
        with self.login("matz", "pythonsucks"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Matz can't see guido's proposal
            self.assertEqual(response.status_code, 302)
        
        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Reviewers can see a review detail page.
            self.assertEqual(response.status_code, 200)
    
    def test_reviewing(self):
        guidos_proposal = Proposal.objects.all()[0]
        
        with self.login("guido", "pythonisawesome"):
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+1",
            })
            # It redirects, but...
            self.assertEqual(response.status_code, 302)
            # ... no vote recorded
            self.assertEqual(guidos_proposal.reviews.count(), 0)
        
        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+0",
                "text": "Looks like a decent proposal, and Guido is a smart guy",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.reviews.count(), 1)
            self.assertEqual(ReviewAssignment.objects.count(), 1)
            assignment = ReviewAssignment.objects.get()
            self.assertEqual(assignment.proposal, guidos_proposal)
            self.assertEqual(assignment.origin, ReviewAssignment.OPT_IN)
            self.assertEqual(guidos_proposal.comments.count(), 1)
            comment = guidos_proposal.comments.get()
            self.assertFalse(comment.public)
            
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+1",
                "text": "Actually Perl is dead, we really need a talk on the future",
            })
            self.assertEqual(guidos_proposal.reviews.count(), 2)
            self.assertEqual(ReviewAssignment.objects.count(), 1)
            assignment = ReviewAssignment.objects.get()
            self.assertEqual(assignment.review, Review.objects.order_by("-id")[0])
            self.assertEqual(guidos_proposal.comments.count(), 2)
            
            # Larry's a big fan...
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+20",
            })
            self.assertEqual(guidos_proposal.reviews.count(), 2)
    
    def test_speaker_commenting(self):
        guidos_proposal = Proposal.objects.all()[0]
        
        with self.login("guido", "pythonisawesome"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Guido can comment on his proposal.
            self.assertEqual(response.status_code, 200)
            
            response = self.post("review_comment", pk=guidos_proposal.pk, data={
                "text": "FYI I can do this as a 30-minute or 45-minute talk.",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.comments.count(), 1)
            comment = guidos_proposal.comments.get()
            self.assertTrue(comment.public)
        
        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Larry can comment, since he's a reviewer
            self.assertEqual(response.status_code, 200)
            
            response = self.post("review_comment", pk=guidos_proposal.pk, data={
                "text": "Thanks for the heads-up Guido."
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.comments.count(), 2)
        
        with self.login("matz", "pythonsucks"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Matz can't comment.
            self.assertEqual(response.status_code, 302)
