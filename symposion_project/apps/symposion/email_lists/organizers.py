from django.contrib.auth.models import User


def email_list():
    for user in User.objects.filter(is_staff=True):
        yield (user.email, {})
