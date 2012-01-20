from fixture_generator import fixture_generator

from symposion.speakers.models import Speaker
from symposion.proposals.models import Proposal


@fixture_generator(Proposal, requires=["speakers.speakers"])
def proposals():
    guido, matz, larry = Speaker.objects.order_by("id")
    
    Proposal.objects.create(
        title = "Django on AppEngine",
        description = "YOU CAN HAVE DJANGO ON THE GOOGLES",
        session_type = Proposal.SESSION_TYPE_TALK,
        audience_level = Proposal.AUDIENCE_LEVEL_NOVICE,
        classification = Proposal.SESSION_CLASSIFICATION_RAISE_AWARENESS,
        speaker = guido,
    )
    
    Proposal.objects.create(
        title = "What Rails can Learn from Django",
        description = "Haha just kidding, what Django can learn from Rails.",
        session_type = Proposal.SESSION_TYPE_TALK,
        audience_level = Proposal.AUDIENCE_LEVEL_EXPERIENCED,
        classification = Proposal.SESSION_CLASSIFICATION_INDEPTH,
        speaker = matz
    )
    
    Proposal.objects.create(
        title = "Why Regular Expressions Are Awesome",
        description = "You guys should totally have a syntax for them",
        session_type = Proposal.SESSION_TYPE_TALK,
        audience_level = Proposal.AUDIENCE_LEVEL_EXPERIENCED,
        classification = Proposal.SESSION_CLASSIFICATION_RAISE_AWARENESS,
        speaker = larry,
    )
