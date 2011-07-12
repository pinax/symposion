from datetime import datetime

from django.core.management.base import BaseCommand

from symposion.schedule.models import Track, Session, Slot


djangocon2011_plenaries = [
    # Tuesday
    [
        {
            "start": datetime(2011, 9, 6, 9, 0),
            "end": datetime(2011, 9, 6, 9, 15),
        },
        {
            "start": datetime(2011, 9, 6, 9, 15),
            "end": datetime(2011, 9, 6, 10, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 6, 12, 0),
            "end": datetime(2011, 9, 6, 13, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 6, 15, 0),
            "end": datetime(2011, 9, 6, 15, 30),
        },
        {
            "start": datetime(2011, 9, 6, 15, 30),
            "end": datetime(2011, 9, 6, 16, 10),
        },
        {
            "start": datetime(2011, 9, 6, 16, 20),
            "end": datetime(2011, 9, 6, 17, 0),
        },
        {
            "start": datetime(2011, 9, 6, 17, 10),
            "end": datetime(2011, 9, 6, 17, 50),
        },
        {
            "start": datetime(2011, 9, 6, 18, 0),
            "end": datetime(2011, 9, 6, 18, 30),
        },
    ],
    # Wednesday
    [
        {
            "start": datetime(2011, 9, 7, 9, 0),
            "end": datetime(2011, 9, 7, 10, 0),
        },
        {
            "start": datetime(2011, 9, 7, 10, 30),
            "end": datetime(2011, 9, 7, 11, 10),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 7, 12, 0),
            "end": datetime(2011, 9, 7, 13, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 7, 15, 0),
            "end": datetime(2011, 9, 7, 15, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 7, 17, 10),
            "end": datetime(2011, 9, 7, 18, 0),
        },
    ],
    # Thrusday
    [
        {
            "start": datetime(2011, 9, 8, 9, 0),
            "end": datetime(2011, 9, 8, 10, 0),
        },
        {
            "start": datetime(2011, 9, 8, 10, 30),
            "end": datetime(2011, 9, 8, 11, 10),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 8, 12, 0),
            "end": datetime(2011, 9, 8, 13, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 8, 15, 0),
            "end": datetime(2011, 9, 8, 15, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 8, 17, 10),
            "end": datetime(2011, 9, 8, 17, 50),
        },
        {
            "start": datetime(2011, 9, 8, 18, 0),
            "end": datetime(2011, 9, 8, 18, 30),
        },
    ],
]

djangocon2011_tuesday_slots = [
    [
        {
            "start": datetime(2011, 9, 6, 10, 30),
            "end": datetime(2011, 9, 6, 11, 10),
        },
        {
            "start": datetime(2011, 9, 6, 11, 20),
            "end": datetime(2011, 9, 6, 12, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 6, 13, 30),
            "end": datetime(2011, 9, 6, 14, 10),
        },
        {
            "start": datetime(2011, 9, 6, 14, 20),
            "end": datetime(2011, 9, 6, 15, 0),
        },
    ],
]

djangocon2011_wednesday_slots = [
    [
        {
            "start": datetime(2011, 9, 7, 11, 20),
            "end": datetime(2011, 9, 7, 12, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 7, 13, 30),
            "end": datetime(2011, 9, 7, 14, 10),
        },
        {
            "start": datetime(2011, 9, 7, 14, 20),
            "end": datetime(2011, 9, 7, 15, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 7, 15, 30),
            "end": datetime(2011, 9, 7, 16, 10),
        },
        {
            "start": datetime(2011, 9, 7, 16, 20),
            "end": datetime(2011, 9, 7, 17, 0),
        },
    ]
]

djangocon2011_thursday_slots = [
    [
        {
            "start": datetime(2011, 9, 8, 11, 20),
            "end": datetime(2011, 9, 8, 12, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 8, 13, 30),
            "end": datetime(2011, 9, 8, 14, 10),
        },
        {
            "start": datetime(2011, 9, 8, 14, 20),
            "end": datetime(2011, 9, 8, 15, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 9, 8, 15, 30),
            "end": datetime(2011, 9, 8, 16, 10),
        },
        {
            "start": datetime(2011, 9, 8, 16, 20),
            "end": datetime(2011, 9, 8, 17, 0),
        },
    ]
]

tracks = [
    {"Track 1": [djangocon2011_tuesday_slots, djangocon2011_wednesday_slots, djangocon2011_thursday_slots]},
    {"Track 2": [djangocon2011_tuesday_slots, djangocon2011_wednesday_slots, djangocon2011_thursday_slots]},
]


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for track_data in tracks:
            for track_name, data in track_data.items():
                track = Track.objects.create(name=track_name)
                print "Created Track: %s" % track_name
                for day in data:
                    for session_data in day:
                        session = Session.objects.create(track=track)
                        print "\tCreated session for %s" % track_name
                        for slot_data in session_data:
                            slot = Slot.objects.create(
                                track=track,
                                session=session,
                                start=slot_data.get("start"),
                                end=slot_data.get("end"),
                                title=slot_data.get("title")
                            )
                            print "\t\tCreated slot: %s" % slot
        print "Plenaries"
        for data in [djangocon2011_plenaries]:
            for session_data in data:
                for slot_data in session_data:
                    slot = Slot.objects.create(
                        track=None,
                        session=None,
                        start=slot_data.get("start"),
                        end=slot_data.get("end"),
                        title=slot_data.get("title")
                    )
                    print "\tCreated slot: %s" % slot
