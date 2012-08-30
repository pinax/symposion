from django.shortcuts import render, get_object_or_404

from symposion.schedule.models import Schedule


def schedule_detail(request, slug=None):
    qs = Schedule.objects.all()
    if slug is None:
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, slug=slug)
    ctx = {
        "schedule": schedule,
    }
    return render(request, "schedule/schedule_detail.html")


def schedule_edit(request, slug=None):
    qs = Schedule.objects.all()
    if slug is None:
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, slug=slug)
    ctx = {
        "schedule": schedule,
    }
    return render(request, "schedule/schedule_edit.html")
