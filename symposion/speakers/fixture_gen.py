from django.contrib.auth.models import User

from fixture_generator import fixture_generator

from symposion.speakers.models import Speaker


@fixture_generator(Speaker, User)
def speakers():
    guido = User.objects.create_user("guido", "guido@python.org", "pythonisawesome")
    matz = User.objects.create_user("matz", "matz@ruby.org", "pythonsucks")
    larry = User.objects.create_user("larryw", "larry@perl.org", "linenoisehere")
    
    Speaker.objects.create(
        user=guido,
        name="Guido van Rossum",
        biography="I wrote Python, and named it after Monty Python",
    )
    Speaker.objects.create(
        user=matz,
        name="Yukihiro Matsumoto",
        biography="I wrote Ruby, and named it after the rare gem Ruby, a pun "
            "on Perl/pearl.",
    )
    Speaker.objects.create(
        user=larry,
        name="Larry Wall",
        biography="I wrote Perl, and named it after the Parable of the Pearl",
    )
