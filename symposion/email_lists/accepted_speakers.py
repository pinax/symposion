def email_list():
    from symposion.schedule.models import Presentation
    speakers = {}
    for presentation in Presentation.objects.select_related("speaker__user"):
        for speaker in presentation.speakers():
            if speaker is not None and speaker.user is not None:
                speakers[speaker.user.email] = {}
    return speakers.iteritems()
