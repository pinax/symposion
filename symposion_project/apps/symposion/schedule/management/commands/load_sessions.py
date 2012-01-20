from datetime import datetime

from django.core.management.base import BaseCommand

from schedule.models import Track, Session, Slot


friday_plenaries = [
    [
        {
            "start": datetime(2011, 3, 11, 7, 0),
            "end": datetime(2011, 3, 11, 8, 0),
        },
        {
            "start": datetime(2011, 3, 11, 8, 0),
            "end": datetime(2011, 3, 11, 9, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 9, 0),
            "end": datetime(2011, 3, 11, 9, 10),
        },
        {
            "start": datetime(2011, 3, 11, 9, 10),
            "end": datetime(2011, 3, 11, 9, 40),
        },
        {
            "start": datetime(2011, 3, 11, 9, 40),
            "end": datetime(2011, 3, 11, 10, 5),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 10, 5),
            "end": datetime(2011, 3, 11, 10, 25),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 17, 30),
            "end": datetime(2011, 3, 11, 18, 0),
        },
    ],
]


friday_slots_type_1 = [
    [
        {
            "start": datetime(2011, 3, 11, 10, 25),
            "end": datetime(2011, 3, 11, 11, 5),
        },
        {
            "start": datetime(2011, 3, 11, 11, 5),
            "end": datetime(2011, 3, 11, 11, 45),
        },
        {
            "start": datetime(2011, 3, 11, 11, 45),
            "end": datetime(2011, 3, 11, 12, 30),
        },
    ],
    [
        {
            "title": "Lunch",
            "start": datetime(2011, 3, 11, 12, 30),
            "end": datetime(2011, 3, 11, 13, 35),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 13, 35),
            "end": datetime(2011, 3, 11, 14, 15),
        },
        {
            "start": datetime(2011, 3, 11, 14, 15),
            "end": datetime(2011, 3, 11, 14, 55),
        },
        {
            "start": datetime(2011, 3, 11, 14, 55),
            "end": datetime(2011, 3, 11, 15, 40),
        },
    ],
    [
        {
            "title": "Afternoon Break with Snacks in Expo Hall",
            "start": datetime(2011, 3, 11, 15, 40),
            "end": datetime(2011, 3, 11, 16, 15),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 16, 15),
            "end": datetime(2011, 3, 11, 16, 55),
        },
        {
            "start": datetime(2011, 3, 11, 16, 55),
            "end": datetime(2011, 3, 11, 17, 30),
        },
    ]
]

friday_slots_type_2 = [
    [
        {
            "start": datetime(2011, 3, 11, 10, 25),
            "end": datetime(2011, 3, 11, 11, 5),
        },
        {
            "start": datetime(2011, 3, 11, 11, 5),
            "end": datetime(2011, 3, 11, 11, 45),
        },
        {
            "start": datetime(2011, 3, 11, 11, 45),
            "end": datetime(2011, 3, 11, 12, 15),
        },
    ],
    [
        {
            "title": "Lunch",
            "start": datetime(2011, 3, 11, 12, 15),
            "end": datetime(2011, 3, 11, 13, 20),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 13, 20),
            "end": datetime(2011, 3, 11, 14, 15),
        },
        {
            "start": datetime(2011, 3, 11, 14, 15),
            "end": datetime(2011, 3, 11, 14, 55),
        },
        {
            "start": datetime(2011, 3, 11, 14, 55),
            "end": datetime(2011, 3, 11, 15, 25),
        },
    ],
    [
        {
            "title": "Afternoon Break with Snacks in Expo Hall",
            "start": datetime(2011, 3, 11, 15, 25),
            "end": datetime(2011, 3, 11, 16, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 11, 16, 0),
            "end": datetime(2011, 3, 11, 16, 55),
        },
        {
            "start": datetime(2011, 3, 11, 16, 55),
            "end": datetime(2011, 3, 11, 17, 30),
        },
    ]
]


saturday_plenaries = [
    [    
        {
            "start": datetime(2011, 3, 12, 7, 0),
            "end": datetime(2011, 3, 12, 8, 0),
        },
        {
            "start": datetime(2011, 3, 12, 8, 0),
            "end": datetime(2011, 3, 12, 8, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 8, 30),
            "end": datetime(2011, 3, 12, 9, 0),
        },
        {
            "start": datetime(2011, 3, 12, 9, 0),
            "end": datetime(2011, 3, 12, 9, 5),
        },
        {
            "start": datetime(2011, 3, 12, 9, 5),
            "end": datetime(2011, 3, 12, 9, 20),
        },
        {
            "start": datetime(2011, 3, 12, 9, 20),
            "end": datetime(2011, 3, 12, 9, 35),
        },
        {
            "start": datetime(2011, 3, 12, 9, 35),
            "end": datetime(2011, 3, 12, 10, 5),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 10, 5),
            "end": datetime(2011, 3, 12, 10, 25),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 17, 30),
            "end": datetime(2011, 3, 12, 18, 0),
        },
    ],
]


saturday_slots_type_1 = [
    [
        {
            "start": datetime(2011, 3, 12, 10, 25),
            "end": datetime(2011, 3, 12, 11, 5),
        },
        {
            "start": datetime(2011, 3, 12, 11, 5),
            "end": datetime(2011, 3, 12, 11, 45),
        },
        {
            "start": datetime(2011, 3, 12, 11, 45),
            "end": datetime(2011, 3, 12, 12, 30),
        },
    ],
    [
        {
            "title": "Lunch",
            "start": datetime(2011, 3, 12, 12, 30),
            "end": datetime(2011, 3, 12, 13, 35),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 13, 35),
            "end": datetime(2011, 3, 12, 14, 15),
        },
        {
            "start": datetime(2011, 3, 12, 14, 15),
            "end": datetime(2011, 3, 12, 14, 55),
        },
        {
            "start": datetime(2011, 3, 12, 14, 55),
            "end": datetime(2011, 3, 12, 15, 40),
        },
    ],
    [
        {
            "title": "Afternoon Break with Snacks in Expo Hall",
            "start": datetime(2011, 3, 12, 15, 40),
            "end": datetime(2011, 3, 12, 16, 15),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 16, 15),
            "end": datetime(2011, 3, 12, 16, 55),
        },
        {
            "start": datetime(2011, 3, 12, 16, 55),
            "end": datetime(2011, 3, 12, 17, 30),
        },
    ]
]

saturday_slots_type_2 = [
    [
        {
            "start": datetime(2011, 3, 12, 10, 25),
            "end": datetime(2011, 3, 12, 11, 5),
        },
        {
            "start": datetime(2011, 3, 12, 11, 5),
            "end": datetime(2011, 3, 12, 11, 45),
        },
        {
            "start": datetime(2011, 3, 12, 11, 45),
            "end": datetime(2011, 3, 12, 12, 15),
        },
    ],
    [
        {
            "title": "Lunch",
            "start": datetime(2011, 3, 12, 12, 15),
            "end": datetime(2011, 3, 12, 13, 20),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 13, 20),
            "end": datetime(2011, 3, 12, 14, 15),
        },
        {
            "start": datetime(2011, 3, 12, 14, 15),
            "end": datetime(2011, 3, 12, 14, 55),
        },
        {
            "start": datetime(2011, 3, 12, 14, 55),
            "end": datetime(2011, 3, 12, 15, 25),
        },
    ],
    [
        {
            "title": "Afternoon Break with Snacks in Expo Hall",
            "start": datetime(2011, 3, 12, 15, 25),
            "end": datetime(2011, 3, 12, 16, 0),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 12, 16, 0),
            "end": datetime(2011, 3, 12, 16, 55),
        },
        {
            "start": datetime(2011, 3, 12, 16, 55),
            "end": datetime(2011, 3, 12, 17, 30),
        },
    ]
]


sunday_plenaries = [
    [    
        {
            "start": datetime(2011, 3, 13, 7, 0),
            "end": datetime(2011, 3, 13, 8, 30),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 13, 8, 30),
            "end": datetime(2011, 3, 13, 9, 0),
        },
        {
            "start": datetime(2011, 3, 13, 9, 0),
            "end": datetime(2011, 3, 13, 9, 5),
        },
        {
            "start": datetime(2011, 3, 13, 9, 5),
            "end": datetime(2011, 3, 13, 9, 20),
        },
        {
            "start": datetime(2011, 3, 13, 9, 20),
            "end": datetime(2011, 3, 13, 9, 35),
        },
        {
            "start": datetime(2011, 3, 13, 9, 35),
            "end": datetime(2011, 3, 13, 10, 5),
        },
    ],
    [
        {
            "title": "Break with Snacks in Poster Area",
            "start": datetime(2011, 3, 13, 10, 5),
            "end": datetime(2011, 3, 13, 10, 25),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 13, 10, 25),
            "end": datetime(2011, 3, 13, 11, 55),
        },
    ],
    [
        {
            "title": "Lunch",
            "start": datetime(2011, 3, 13, 12, 25),
            "end": datetime(2011, 3, 13, 13, 15),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 13, 14, 35),
            "end": datetime(2011, 3, 13, 15, 35),
        },
        {
            "start": datetime(2011, 3, 13, 15, 35),
            "end": datetime(2011, 3, 13, 15, 55),
        },
    ],
]

sunday_type_1 = [
    [
        {
            "start": datetime(2011, 3, 13, 11, 55),
            "end": datetime(2011, 3, 13, 12, 25),
        },
    ],
    [
        {
            "start": datetime(2011, 3, 13, 13, 15),
            "end": datetime(2011, 3, 13, 13, 55),
        },
        {
            "start": datetime(2011, 3, 13, 13, 55),
            "end": datetime(2011, 3, 13, 14, 35),
        },
    ],
]


tracks = [
    {"Centennial I": [friday_slots_type_1, saturday_slots_type_1, sunday_type_1]},
    {"Centennial II": [friday_slots_type_2, saturday_slots_type_2, sunday_type_1]},
    {"Centennial III": [friday_slots_type_1, saturday_slots_type_1, sunday_type_1]},
    {"Centennial IV": [friday_slots_type_2, saturday_slots_type_2, sunday_type_1]},
    {"Regency V": [friday_slots_type_1, saturday_slots_type_1, sunday_type_1]}
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
        for data in [friday_plenaries, saturday_plenaries, sunday_plenaries]:
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
