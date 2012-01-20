from cStringIO import StringIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from eldarion_test import TestCase

from symposion.sponsors_pro.models import Sponsor, Benefit, SponsorLevel, BenefitLevel


class SponsorTests(TestCase):
    def setUp(self):
        self.linus = User.objects.create_user("linus", "linus@linux.org", "penguin")
        self.kant = User.objects.create_user("kant", "immanuel@kant.org", "justice")
    
    def test_index(self):
        response = self.get("sponsor_index")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<li class="next"><a href="/2011/account/signup/')
        
        with self.login("linus", "penguin"):
            response = self.get("sponsor_index")
            self.assertContains(response, '<li class="next"><a href="/2011/sponsors/apply/')
            
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org"
            })
            self.assertEqual(response.status_code, 302)
            
            response = self.get("sponsor_index")
            self.assertContains(response, "Your sponsorship application is being processed.")
            
            s = Sponsor.objects.get()
            s.active = True
            s.save()
            
            response = self.get("sponsor_index")
            self.assertEqual(response.status_code, 302)
    
    def test_apply(self):
        response = self.get("sponsor_apply")
        self.assertEqual(response.status_code, 302)
        
        with self.login("linus", "penguin"):
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Sponsor.objects.count(), 0)

            response = self.get("sponsor_apply")
            self.assertEqual(response.status_code, 200)
            
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org",
            })
            self.assertEqual(response.status_code, 302)
            s = Sponsor.objects.get()
            self.assertEqual(s.applicant, self.linus)
            self.assertEqual(s.active, None)
            
            response = self.get("sponsor_apply")
            self.assertEqual(response.status_code, 302)
    
    def test_detail(self):
        with self.login("linus", "penguin"):
            self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org",
            })
            s = Sponsor.objects.get()
            
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 302)

            s.active = True
            s.save()
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 200)
        
        with self.login("kant", "justice"):
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 302)
        
        response = self.get("sponsor_detail", pk=s.pk)
        self.assertEqual(response.status_code, 302)


    def test_detail_edit(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   active=True)

        detail_url = reverse("sponsor_detail", kwargs={'pk': s.pk})
        
        with self.login("linus", "penguin"):
            # @@@ yuck. would love to clean this up using
            # http://pythonpaste.org/webtest/#id2 and
            # http://pypi.python.org/pypi/django-webtest/
            response = self.client.post(detail_url,
                                        {'name': 'Linux Fund',
                                         'external_url': 'http://www.linuxfund.org',
                                         'contact_name': 'Randal Schwartz',
                                         'contact_email': 'randal@schwartz.org',
                                         'sponsor_benefits-TOTAL_FORMS': '0',
                                         'sponsor_benefits-INITIAL_FORMS': '0',
                                         })
            self.assertRedirects(response, detail_url)

            self.assertEqual(self.reload(s).name, 'Linux Fund')

        
class BenefitTests(TestCase):
    def setUp(self):
        self.linus = User.objects.create_user("linus", "linus@linux.org", "penguin")

        self.tin = SponsorLevel.objects.create(name='Tin', cost=10000, order=0)
        self.zinc = SponsorLevel.objects.create(name='Zinc', cost=5000, order=1)
        self.lead = SponsorLevel.objects.create(name='Lead', cost=2000, order=2)

        self.cookies = Benefit.objects.create(name='Cookies', type='simple')
        self.free_speech = Benefit.objects.create(name='Free Speech', type='text')
        self.mugshot = Benefit.objects.create(name='Mugshot', type='file')

        BenefitLevel.objects.create(level=self.tin, benefit=self.cookies,
                                    other_limits='all you can eat')
        BenefitLevel.objects.create(level=self.tin, benefit=self.free_speech,
                                    max_words=100)
        BenefitLevel.objects.create(level=self.tin, benefit=self.mugshot,
                                    other_limits='b&w, 2x2in, unflattering')
        BenefitLevel.objects.create(level=self.zinc, benefit=self.cookies,
                                    other_limits='only one')
        BenefitLevel.objects.create(level=self.lead, benefit=self.cookies,
                                    other_limits='crumbs')

    def check_benefits(self, sponsor, benefits):
        self.assertEqual([(unicode(b.benefit),
                           b.max_words, b.other_limits, b.active)
                          for b in sponsor.sponsor_benefits.all()],
                         benefits)
        
    def test_reset_benefits(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   level=self.zinc)
        self.check_benefits(s, [('Cookies', None, 'only one', True)])

        s.level = self.tin
        s.save()

        self.check_benefits(s, [('Cookies', None, 'all you can eat', True),
                                ('Free Speech', 100, '', True),
                                ('Mugshot', None, 'b&w, 2x2in, unflattering', True)])

        s.level = self.lead
        s.save()

        self.check_benefits(s, [('Cookies', None, 'crumbs', True),
                                ('Free Speech', None, '', False),
                                ('Mugshot', None, '', False)])

        s.level = self.tin
        s.save()

        self.check_benefits(s, [('Cookies', None, 'all you can eat', True),
                                ('Free Speech', 100, '', True),
                                ('Mugshot', None, 'b&w, 2x2in, unflattering', True)])

        s.level = None
        s.save()
        
        self.check_benefits(s, [('Cookies', None, '', False),
                                ('Free Speech', None, '', False),
                                ('Mugshot', None, '', False)])

    def test_enforce_max_words(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   level=self.tin)

        sb = s.sponsor_benefits.get(benefit=self.free_speech)
        sb.text = 'FIRE! ' * 99
        sb.clean()
        sb.text = 'FIRE! ' * 101
        self.assertRaises(ValidationError, sb.clean)

    def test_edit_benefits(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   active=True, level=self.tin)

        detail_url = reverse("sponsor_detail", kwargs={'pk': s.pk})
        
        with self.login("linus", "penguin"):
            # @@@ yuck. would love to clean this up using
            # http://pythonpaste.org/webtest/#id2 and
            # http://pypi.python.org/pypi/django-webtest/
            upload = SimpleUploadedFile('somefile.txt', 'some file data')
            response = self.client.post(detail_url,
                                        {'name': 'Linux Fund',
                                         'external_url': 'http://www.linuxfund.org',
                                         'contact_name': 'Randal Schwartz',
                                         'contact_email': 'randal@schwartz.org',
                                         'sponsor_benefits-TOTAL_FORMS': '3',
                                         'sponsor_benefits-INITIAL_FORMS': '3',
                                         'sponsor_benefits-0-id': '1',
                                         'sponsor_benefits-1-id': '2',
                                         'sponsor_benefits-1-text': 'FIRE!',
                                         'sponsor_benefits-2-id': '3',
                                         'sponsor_benefits-2-upload': upload})
            self.assertRedirects(response, detail_url)

            self.assertEqual(self.reload(s).name, 'Linux Fund')

