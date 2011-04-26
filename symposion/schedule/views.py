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

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from schedule.cache import db, cache_key_user
from schedule.forms import PlenaryForm, RecessForm, PresentationForm
from schedule.models import Slot, Presentation, Track, Session, SessionRole, UserBookmark


wed_morn_start = datetime.datetime(2011, 3, 9, 9, 0)  # 9AM Eastern
wed_morn_end = datetime.datetime(2011, 3, 9, 12, 20)  # 12:20PM Eastern
wed_after_start = datetime.datetime(2011, 3, 9, 13, 20)  # 1:20PM Eastern
wed_after_end = datetime.datetime(2011, 3, 9, 16, 40)  # 4:40PM Eastern
thu_morn_start = datetime.datetime(2011, 3, 10, 9, 0)  # 9AM Eastern
thu_morn_end = datetime.datetime(2011, 3, 10, 12, 20)  # 12:20PM Eastern
thu_after_start = datetime.datetime(2011, 3, 10, 13, 20)  # 1:20PM Eastern
thu_after_end = datetime.datetime(2011, 3, 10, 16, 40)  # 4:40PM Eastern

WEDNESDAY_MORNING = (wed_morn_start, wed_morn_end)
WEDNESDAY_AFTERNOON = (wed_after_start, wed_after_end)
THURSDAY_MORNING = (thu_morn_start, thu_morn_end)
THURSDAY_AFTERNOON = (thu_after_start, thu_after_end)


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
    
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    if request.user.is_authenticated():
        bookmarks = UserBookmark.objects.filter(
            user=request.user, presentation=presentation
        )
        presentation.bookmarked = bookmarks.exists()
    
    return render_to_response(template_name, dict({
        "presentation": presentation,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_list_talks(request):
    
    talks = Presentation.objects.filter(
        presentation_type__in=[Presentation.PRESENTATION_TYPE_PANEL, Presentation.PRESENTATION_TYPE_TALK]
    )
    talks = talks.order_by("pk")
    
    return render_to_response("schedule/list_talks.html", dict({
        "talks": talks,
    }), context_instance=RequestContext(request))


def schedule_list_tutorials(request):
    
    tutorials = Presentation.objects.filter(
        presentation_type=Presentation.PRESENTATION_TYPE_TUTORIAL
    )
    tutorials = tutorials.order_by("pk")
    
    return render_to_response("schedule/list_tutorials.html", dict({
        "tutorials": tutorials,
    }), context_instance=RequestContext(request))


def schedule_list_posters(request):
    
    posters = Presentation.objects.filter(
        presentation_type=Presentation.PRESENTATION_TYPE_POSTER
    )
    posters = posters.order_by("pk")
    
    return render_to_response("schedule/list_posters.html", dict({
        "posters": posters,
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
        "friday": Timetable(Slot.objects.filter(start__week_day=6), user=request.user),
        "saturday": Timetable(Slot.objects.filter(start__week_day=7), user=request.user),
        "sunday": Timetable(Slot.objects.filter(start__week_day=1), user=request.user),
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
        "friday": Timetable(Slot.objects.filter(start__week_day=6), user=request.user),
        "saturday": Timetable(Slot.objects.filter(start__week_day=7), user=request.user),
        "sunday": Timetable(Slot.objects.filter(start__week_day=1), user=request.user),
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
            data += "NO SPEAKER DATA (contact e-mail: %s)" % speaker.invite_email
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
