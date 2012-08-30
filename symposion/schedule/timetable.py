import itertools

from symposion.schedule.models import Room, Slot


class TimeTable(object):
    
    def __init__(self, day):
        self.day = day
    
    def slots_qs(self):
        return Slot.objects.filter(day=self.day)
    
    def rooms(self):
        return Room.objects.filter(schedule=self.day.schedule).order_by("order")
    
    def __iter__(self):
        times = sorted(set(itertools.chain(*self.slots_qs().values_list("start", "end"))))
        slots = list(self.slots_qs().order_by("start"))
        row = []
        for time, next_time in pairwise(times):
            row = {"time": time, "slots": []}
            for slot in slots:
                if slot.start == time:
                    slot.rowspan = TimeTable.rowspan(times, slot.start, slot.end)
                    row["slots"].append(slot)
            row["colspan"] = self.rooms.consecutive_count()
            if row["slots"] or next_time is None:
                yield row
    
    @staticmethod
    def rowspan(times, start, end):
        return times.index(end) - times.index(start)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    b.next()
    return itertools.izip_longest(a, b)
