import datetime
import hashlib
import itertools

from icalendar import Calendar, Event

from django.conf import settings
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import simplejson as json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from symposion.conference.models import PresentationKind

from symposion.schedule.cache import db, cache_key_user
from symposion.schedule.forms import PlenaryForm, RecessForm, PresentationForm
from symposion.schedule.models import (Slot, Presentation, Track, Session, SessionRole,
    UserBookmark, Plenary)


# @@@ this needs some rethinking (PyCon 2012 specific and hacky as heck)
wed_morn_start = datetime.datetime(2012, 3, 7, 12, 0)  # 9AM Pacific
wed_morn_end = datetime.datetime(2012, 3, 7, 15, 20)  # 12:20PM Pacific
wed_after_start = datetime.datetime(2012, 3, 7, 16, 20)  # 1:20PM Pacific
wed_after_end = datetime.datetime(2012, 3, 7, 19, 40)  # 4:40PM Pacific
thu_morn_start = datetime.datetime(2012, 3, 8, 12, 0)  # 9AM Pacific
thu_morn_end = datetime.datetime(2012, 3, 8, 15, 20)  # 12:20PM Pacific
thu_after_start = datetime.datetime(2012, 3, 8, 16, 20)  # 1:20PM Pacific
thu_after_end = datetime.datetime(2012, 3, 8, 19, 40)  # 4:40PM Pacific

WEDNESDAY_MORNING = (wed_morn_start, wed_morn_end)
WEDNESDAY_AFTERNOON = (wed_after_start, wed_after_end)
THURSDAY_MORNING = (thu_morn_start, thu_morn_end)
THURSDAY_AFTERNOON = (thu_after_start, thu_after_end)

CONFERENCE_TAGS = getattr(settings, "CONFERENCE_TAGS", [])


def hash_for_user(user):
    return hashlib.sha224(settings.SECRET_KEY + user.username).hexdigest()


def schedule_list(request, template_name="schedule/schedule_list.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    slots = Slot.objects.all().order_by("start")
    
    return render_to_response(template_name, dict({
        "slots": slots,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_presentation(request, presentation_id, template_name="schedule/presentation_detail.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    presentation = get_object_or_404(Presentation, id=presentation_id, kind__published=True)
    
    if request.user.is_authenticated():
        bookmarks = UserBookmark.objects.filter(
            user=request.user, presentation=presentation
        )
        presentation.bookmarked = bookmarks.exists()
    
    return render_to_response(template_name, dict({
        "presentation": presentation,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_presentation_list(request, kind_slug):

    kind = get_object_or_404(PresentationKind, slug=kind_slug, published=True)
    talks = Presentation.objects.filter(kind=kind, cancelled=False).order_by("pk")

    return render_to_response("schedule/list_presentations.html", dict({
        "talks": talks,
        "kind": kind,
    }), context_instance=RequestContext(request))


def schedule_tutorials(request):
    
    tutorials = {
        "wed": {
            "morning": {
                "slot": WEDNESDAY_MORNING,
                "presentations": Presentation.objects.filter(
                    slot__start=WEDNESDAY_MORNING[0]
                ).order_by("pk"),
            },
            "afternoon": {
                "slot": WEDNESDAY_AFTERNOON,
                "presentations": Presentation.objects.filter(
                    slot__start=WEDNESDAY_AFTERNOON[0]
                ).order_by("pk"),
            }
        },
        "thurs": {
            "morning": {
                "slot": THURSDAY_MORNING,
                "presentations": Presentation.objects.filter(
                    slot__start=THURSDAY_MORNING[0]
                ).order_by("pk"),
            },
            "afternoon": {
                "slot": THURSDAY_AFTERNOON,
                "presentations": Presentation.objects.filter(
                    slot__start=THURSDAY_AFTERNOON[0]
                ).order_by("pk"),
            }
        }
    }
    
    ctx = {
        "tutorials": tutorials,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/tutorials.html", ctx)


def izip_longest(*args):
    fv = None
    def sentinel(counter=([fv]*(len(args)-1)).pop):
        yield counter()
    iters = [itertools.chain(it, sentinel(), itertools.repeat(fv)) for it in args]
    try:
        for tup in itertools.izip(*iters):
            yield tup
    except IndexError:
        pass


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    b.next()
    return izip_longest(a, b)


class Timetable(object):
    
    def __init__(self, slots, user=None):
        self.slots = slots
        
        if user.is_authenticated():
            self.user = user
        else:
            self.user = None
    
    @property
    def tracks(self):
        return Track.objects.filter(
            pk__in = self.slots.exclude(track=None).values_list("track", flat=True).distinct()
        ).order_by("name")
    
    def __iter__(self):
        times = sorted(set(itertools.chain(*self.slots.values_list("start", "end"))))
        slots = list(self.slots.order_by("start", "track__name"))
        row = []
        for time, next_time in pairwise(times):
            row = {"time": time, "slots": []}
            for slot in slots:
                if slot.start == time:
                    slot.rowspan = Timetable.rowspan(times, slot.start, slot.end)
                    if self.user and (slot.kind and slot.kind.name == "presentation"):
                        bookmarks = UserBookmark.objects.filter(
                            user=self.user, presentation=slot.content()
                        )
                        slot.bookmarked = bookmarks.exists()
                    row["slots"].append(slot)
            if len(row["slots"]) == 1:
                row["colspan"] = len(self.tracks)
            else:
                row["colspan"] = 1
            if row["slots"] or next_time is None:
                yield row
    
    @staticmethod
    def rowspan(times, start, end):
        return times.index(end) - times.index(start)


@login_required
def schedule_conference_edit(request):
    if not request.user.is_staff:
        return redirect("schedule_conference")
    ctx = {
        "timetables": [
            Timetable(Slot.objects.filter(start__week_day=3), user=request.user),
            Timetable(Slot.objects.filter(start__week_day=4), user=request.user),
            Timetable(Slot.objects.filter(start__week_day=5), user=request.user),
        ],
        "timezone": settings.SCHEDULE_TIMEZONE,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/conference_edit.html", ctx)


def schedule_conference(request):
    
    if request.user.is_authenticated():
        user_hash = hash_for_user(request.user)
    else:
        user_hash = None
    
    ctx = {
        "user_hash": user_hash,
        "timetables": [
            Timetable(Slot.objects.filter(start__week_day=3), user=request.user),
            Timetable(Slot.objects.filter(start__week_day=4), user=request.user),
            Timetable(Slot.objects.filter(start__week_day=5), user=request.user),
        ],
        "timezone": settings.SCHEDULE_TIMEZONE,
        "csrf_token": csrf(request),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/conference.html", ctx)


@login_required
def schedule_slot_add(request, slot_id, kind):
    
    if not request.user.is_staff:
        return redirect("/")
    
    slot = Slot.objects.get(pk=slot_id)
    
    form_class = {
        "plenary": PlenaryForm,
        "break": RecessForm,
        "presentation": PresentationForm,
    }[kind]
    
    if request.method == "POST":
        form = form_class(request.POST)
        
        if form.is_valid():
            slot_content = form.save(commit=False)
            slot.assign(slot_content)
            return redirect("schedule_conference_edit")
    else:
        form = form_class()
    
    ctx = {
        "slot": slot,
        "kind": kind,
        "form": form,
        "add": True,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/slot_place.html", ctx)


@login_required
def schedule_slot_edit(request, slot_id):
    
    if not request.user.is_staff:
        return redirect("/")
    
    slot = Slot.objects.get(pk=slot_id)
    kind = slot.kind.name
    
    form_tuple = {
        "plenary": (PlenaryForm, {"instance": slot.content()}),
        "recess": (RecessForm, {"instance": slot.content()}),
        "presentation": (PresentationForm, {"initial": {"presentation": slot.content()}}),
    }[kind]
    
    if request.method == "POST":
        form = form_tuple[0](request.POST, **form_tuple[1])
        
        if form.is_valid():
            slot_content = form.save(commit=False)
            slot.assign(slot_content, old_content=slot.content())
            return redirect("schedule_conference_edit")
    else:
        form = form_tuple[0](**form_tuple[1])
    
    ctx = {
        "slot": slot,
        "kind": kind,
        "form": form,
        "add": False,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/slot_place.html", ctx)


@login_required
def schedule_slot_remove(request, slot_id):
    
    if not request.user.is_staff:
        return redirect("/")
    
    slot = Slot.objects.get(pk=slot_id)
    
    if request.method == "POST":
        slot.unassign()
        return redirect("schedule_conference_edit")
    
    ctx = {
        "slot": slot,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/slot_remove.html", ctx)


def track_list(request):
    
    tracks = Track.objects.order_by("name")
    
    return render_to_response("schedule/track_list.html", {
        "tracks": tracks,
    }, context_instance=RequestContext(request))


def track_detail(request, track_id):
    
    track = get_object_or_404(Track, id=track_id)
    
    return render_to_response("schedule/track_detail.html", {
        "track": track,
    }, context_instance=RequestContext(request))


def track_detail_none(request):
    
    sessions = Session.objects.filter(track=None)
    slots = Slot.objects.filter(track=None)
    
    return render_to_response("schedule/track_detail_none.html", {
        "sessions": sessions,
        "slots": slots,
    }, context_instance=RequestContext(request))


def session_list(request):
    
    sessions = Session.objects.all()
    
    return render_to_response("schedule/session_list.html", {
        "sessions": sessions,
    }, context_instance=RequestContext(request))


def session_detail(request, session_id):
    
    session = get_object_or_404(Session, id=session_id)
    
    chair = None
    chair_denied = False
    chairs = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR).exclude(status=False)
    if chairs:
        chair = chairs[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_CHAIR, status=False):
                chair_denied = True
    
    runner = None
    runner_denied = False
    runners = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER).exclude(status=False)
    if runners:
        runner = runners[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_RUNNER, status=False):
                runner_denied = True
    
    if request.method == "POST" and request.user.is_authenticated():
        role = request.POST.get("role")
        if role == "chair":
            if chair == None and not chair_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user).save()
        elif role == "runner":
            if runner == None and not runner_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user).save()
        elif role == "un-chair":
            if chair == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user)
                if session_role:
                    session_role[0].delete()
        elif role == "un-runner":
            if runner == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user)
                if session_role:
                    session_role[0].delete()
        
        return redirect("schedule_session_detail", session_id)
    
    return render_to_response("schedule/session_detail.html", {
        "session": session,
        "chair": chair,
        "chair_denied": chair_denied,
        "runner": runner,
        "runner_denied": runner_denied,
    }, context_instance=RequestContext(request))


@login_required
def schedule_user_slot_manage(request, presentation_id):
    if request.method == "POST":
        if request.POST["action"] == "add":
            try:
                UserBookmark.objects.create(user=request.user, presentation_id=presentation_id)
            except IntegrityError:
                pass
        elif request.POST["action"] == "delete":
            UserBookmark.objects.filter(user=request.user, presentation=presentation_id).delete()
        else:
            return HttpResponse(status=400)
        if db:
            db.delete(cache_key_user(request.user))
        return HttpResponse(status=202)
    else:
        return HttpResponseNotAllowed(["POST"])


@staff_member_required
def schedule_export_speaker_data(request):
    speakers = set()
    data = ""
    
    for presentation in Presentation.objects.all():
        speakers.add(presentation.speaker)
        for speaker in presentation.additional_speakers.all():
            speakers.add(speaker)
    
    for speaker in speakers:
        if speaker.user_id is None:
            data += "NO SPEAKER DATA (contact email: %s)" % speaker.invite_email
        else:
            data += "%s\n\n%s" % (speaker.name.strip(), speaker.biography.strip())
        data += "\n\n%s\n\n" % ("-"*80)
    
    return HttpResponse(data, content_type="text/plain;charset=UTF-8")


def schedule_export_panels(request):
    data = ""
    for presentation in Presentation.objects.filter(presentation_type=Presentation.PRESENTATION_TYPE_PANEL):
        data += "%s\n" % presentation.title
    return HttpResponse(data, content_type="text/plain;charset=UTF-8")


def schedule_user_bookmarks(request, user_id, user_hash):
    
    user = get_object_or_404(User, id=user_id)
    auth_hash = hash_for_user(user)
    
    if user_hash != auth_hash:
        raise Http404()
    
    bookmarks = UserBookmark.objects.filter(user=user)
    
    cal = Calendar()
    cal.add("prodid", "-//PyCon 2011 Bookmarks//us.pycon.org//EN")
    cal.add("version", "2.0")
    cal.add("method", "REQUEST")
    cal.add("calscale", "GREGORIAN")
    cal.add("X-WR-CALNAME", "PyCon 2011 Bookmarks - %s" % user.username)
    cal.add("X-WR-TIMEZONE","US/Eastern")
    
    for bookmark in bookmarks:
        p = bookmark.presentation
        if p.slot is not None:
            event = Event()
            event.add("summary", p.title)
            event.add("dtstart", p.slot.start)
            event.add("dtend", p.slot.end)
            event.add("dtstamp", datetime.datetime.utcnow())
            event.add("description", p.speaker.name + "\n\n" + p.description)
            event.add("location", p.slot.track)
            event["uid"] = str(p.pk) + "-2011.us.pycon.org"
            cal.add_component(event)
    
    response = HttpResponse(cal.as_string(), content_type="text/calendar")
    response["Content-Disposition"] = "filename=pycon2011-%s-bookmarks.ics" % user.username.encode("utf-8")
    return response

def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return list(obj.timetuple())
    raise TypeError

def schedule_json(request):
    slots = Slot.objects.all().order_by("start")

    data = []
    for slot in slots:
        try:
            tags = []
            tags.append(slot.presentation.presentation_type.slug)
            tags.append(Presentation.AUDIENCE_LEVELS[slot.presentation.audience_level - 1][1].lower())
            tags.extend(CONFERENCE_TAGS)
            data.append({
                "room": slot.track.name,
                "start": slot.start,
                "duration": (slot.end - slot.start).seconds // 60,
                "end": slot.end,
                "title": slot.presentation.title,
                "name": slot.presentation.title,
                "presenters": ", ".join(map(
                    lambda s: s.name,
                    slot.presentation.speakers()
                )),
                "description": slot.presentation.description,
                "abstract": slot.presentation.abstract,
                "id": slot.pk,
                "url": "http://%s%s" % (Site.objects.get_current().domain, slot.presentation.get_absolute_url()),
                "tags": ", ".join(tags),
                "last_updated": slot.presentation.last_updated,

                # Add some fields for Carl
                "license": "",
                "conf_url": "",
                "conf_key": "",
                "released": True,
                "start_iso": slot.start.isoformat(),
                "end_iso": slot.end.isoformat(),
                "authors": ", ".join(map(
                    lambda s: s.name,
                    slot.presentation.speakers()
                )),
                "last_updated_iso": slot.presentation.last_updated.isoformat(),
                "contact": "", # not sure if this is ok to be shared.
            })
        except Presentation.DoesNotExist:
            try:
                data.append({
                    "room": "Plenary",
                    "start": slot.start,
                    "duration": (slot.end - slot.start).seconds // 60,
                    "end": slot.end,
                    "title": slot.plenary.title,
                    "name": slot.plenary.title,
                    "presenters": ", ".join(map(
                        lambda s: s.name if s else "",
                        slot.plenary.speakers()
                    )),
                    "description": slot.plenary.description,
                    "abstract": None,
                    "id": slot.pk,
                    "url": None,
                    "tags": "plenary",
                    "last_updated": slot.plenary.last_updated,

                    # Add some fields for Carl
                    "license": "",
                    "conf_url": "",
                    "conf_key": "",
                    "start_iso": slot.start.isoformat(),
                    "end_iso": slot.end.isoformat(),
                    "released": True,
                    "authors": ", ".join(map(
                        lambda s: s.name if s else "",
                        slot.plenary.speakers()
                    )),
                    "last_updated_iso": slot.plenary.last_updated,
                    "contact": "", # not sure if this is ok to be shared.

                })
            except Plenary.DoesNotExist:
                pass

    return HttpResponse(
        json.dumps(data, default=json_serializer),
        content_type="application/json"
    )
