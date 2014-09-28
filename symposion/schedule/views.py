import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader, Context

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from symposion.schedule.forms import SlotEditForm
from symposion.schedule.models import Schedule, Day, Slot, Presentation
from symposion.schedule.timetable import TimeTable


def fetch_schedule(slug):
    qs = Schedule.objects.all()

    if slug is None:
        if qs.count() > 1:
            raise Http404()
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, section__slug=slug)

    return schedule


def schedule_conference(request):

    schedules = Schedule.objects.filter(published=True, hidden=False)

    sections = []
    for schedule in schedules:
        days_qs = Day.objects.filter(schedule=schedule)
        days = [TimeTable(day) for day in days_qs]
        sections.append({
            "schedule": schedule,
            "days": days,
        })

    ctx = {
        "sections": sections,
    }
    return render(request, "schedule/schedule_conference.html", ctx)


def schedule_detail(request, slug=None):

    schedule = fetch_schedule(slug)
    if not schedule.published and not request.user.is_staff:
        raise Http404()

    days_qs = Day.objects.filter(schedule=schedule)
    days = [TimeTable(day) for day in days_qs]

    ctx = {
        "schedule": schedule,
        "days": days,
    }
    return render(request, "schedule/schedule_detail.html", ctx)


def schedule_list(request, slug=None):
    schedule = fetch_schedule(slug)

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True)

    ctx = {
        "schedule": schedule,
        "presentations": presentations,
    }
    return render(request, "schedule/schedule_list.html", ctx)


def schedule_list_csv(request, slug=None):
    schedule = fetch_schedule(slug)

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True).order_by("id")

    response = HttpResponse(mimetype="text/csv")
    if slug:
        file_slug = slug
    else:
        file_slug = "presentations"
    response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_slug

    response.write(loader.get_template("schedule/schedule_list.csv").render(Context({
        "presentations": presentations,

    })))
    return response


@login_required
def schedule_edit(request, slug=None):

    if not request.user.is_staff:
        raise Http404()

    schedule = fetch_schedule(slug)

    days_qs = Day.objects.filter(schedule=schedule)
    days = [TimeTable(day) for day in days_qs]
    ctx = {
        "schedule": schedule,
        "days": days,
    }
    return render(request, "schedule/schedule_edit.html", ctx)


@login_required
def schedule_slot_edit(request, slug, slot_pk):

    if not request.user.is_staff:
        raise Http404()

    slot = get_object_or_404(Slot, day__schedule__section__slug=slug, pk=slot_pk)

    if request.method == "POST":
        form = SlotEditForm(request.POST, slot=slot)
        if form.is_valid():
            save = False
            if "content_override" in form.cleaned_data:
                slot.content_override = form.cleaned_data["content_override"]
                save = True
            if "presentation" in form.cleaned_data:
                presentation = form.cleaned_data["presentation"]
                if presentation is None:
                    slot.unassign()
                else:
                    slot.assign(presentation)
            if save:
                slot.save()
        return redirect("schedule_edit", slug)
    else:
        form = SlotEditForm(slot=slot)
        ctx = {
            "slug": slug,
            "form": form,
            "slot": slot,
        }
        return render(request, "schedule/_slot_edit.html", ctx)


def schedule_presentation_detail(request, pk):

    presentation = get_object_or_404(Presentation, pk=pk)
    if presentation.slot:
        schedule = presentation.slot.day.schedule
    else:
        schedule = None

    ctx = {
        "presentation": presentation,
        "schedule": schedule,
    }
    return render(request, "schedule/presentation_detail.html", ctx)


def schedule_json(request):
    slots = Slot.objects.filter(
        day__schedule__published=True,
        day__schedule__hidden=False
    ).order_by("start")

    protocol = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
    data = []
    for slot in slots:
        slot_data = {
            "room": ", ".join(room["name"] for room in slot.rooms.values()),
            "rooms": [room["name"] for room in slot.rooms.values()],
            "start": slot.start_datetime.isoformat(),
            "end": slot.end_datetime.isoformat(),
            "duration": slot.length_in_minutes,
            "kind": slot.kind.label,
            "section": slot.day.schedule.section.slug,
            "conf_key": slot.pk,
            # TODO: models should be changed.
            # these are model features from other conferences that have forked symposion
            # these have been used almost everywhere and are good candidates for
            # base proposals
            "license": "CC BY",
            "tags": "",
            "released": True,
            "contact": [],


        }
        if hasattr(slot.content, "proposal"):
            slot_data.update({
                "name": slot.content.title,
                "authors": [s.name for s in slot.content.speakers()],
                "contact": [
                    s.email for s in slot.content.speakers()
                ] if request.user.is_staff else ["redacted"],
                "abstract": slot.content.abstract.raw,
                "description": slot.content.description.raw,
                "conf_url": "%s://%s%s" % (
                    protocol,
                    Site.objects.get_current().domain,
                    reverse("schedule_presentation_detail", args=[slot.content.pk])
                ),
                "cancelled": slot.content.cancelled,
            })
        else:
            slot_data.update({
                "name": slot.content_override.raw if slot.content_override else "Slot",
            })
        data.append(slot_data)

    return HttpResponse(
        json.dumps({'schedule': data}),
        content_type="application/json"
    )
