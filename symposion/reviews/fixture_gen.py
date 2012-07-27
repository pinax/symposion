from django.contrib.auth.models import Group

from fixture_generator import fixture_generator


@fixture_generator(Group)
def initial_data():
    Group.objects.create(name="reviewers")
    Group.objects.create(name="reviewers-admins")
