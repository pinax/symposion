from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from symposion.schedule.forms import SlotEditForm
from symposion.schedule.models import Schedule, Day, Slot, Presentation
from symposion.schedule.timetable import TimeTable


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
    return render(request, "schedule/schedule_detail.html", ctx)


def schedule_list(request):
    presentations = Presentation.objects.exclude(cancelled=True).order_by("id")
    ctx = {
        "presentations": presentations,
    }
    return render(request, "schedule/schedule_list.html", ctx)


@login_required
def schedule_edit(request, slug=None):
    
    if not request.user.is_staff:
        raise Http404()
    
    qs = Schedule.objects.all()
    
    if slug is None:
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, slug=slug)
    
    days_qs = Day.objects.filter(schedule=schedule)
    days = [TimeTable(day) for day in days_qs]
    ctx = {
        "schedule": schedule,
        "days": days,
    }
    return render(request, "schedule/schedule_edit.html", ctx)


@login_required
def schedule_slot_edit(request, slot_pk):
    
    if not request.user.is_staff:
        raise Http404()
    
    slot = get_object_or_404(Slot, pk=slot_pk)
    
    # slot content
    try:
        content = slot.content
    except ObjectDoesNotExist:
        content = None
    
    if request.method == "POST":
        form = SlotEditForm(request.POST, content=content)
        if form.is_valid():
            presentation = form.cleaned_data["presentation"]
            if presentation is None:
                slot.unassign()
            else:
                slot.assign(presentation)
        return redirect("schedule_edit_singleton")
    else:
        form = SlotEditForm(content=content)
        ctx = {
            "form": form,
            "slot": slot,
        }
        return render(request, "schedule/_slot_edit.html", ctx)
