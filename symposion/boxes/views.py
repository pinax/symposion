from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from symposion.boxes.authorization import load_can_edit
from symposion.boxes.forms import BoxForm
from symposion.boxes.models import Box


# @@@ problem with this is that the box_edit.html and box_create.html won't have domain objects in context
def get_auth_vars(request):
    auth_vars = {}
    if request.method == "POST":
        keys = [k for k in request.POST.keys() if k.startswith("boxes_auth_")]
        for key in keys:
            auth_vars[key.replace("boxes_auth_", "")] = request.POST.get(key)
        auth_vars["user"] = request.user
    return auth_vars


@require_POST
def box_edit(request, label):
    
    if not load_can_edit()(request, **get_auth_vars(request)):
        return HttpResponseForbidden()
    
    next = request.GET.get("next")
    
    try:
        box = Box.objects.get(label=label)
    except Box.DoesNotExist:
        box = None
    
    form = BoxForm(request.POST, instance=box, prefix=label)

    if form.is_valid():
        if box is None:
            box = form.save(commit=False)
            box.label = label
            box.created_by = request.user
            box.last_updated_by = request.user
            box.save()
        else:
            form.save()
        return redirect(next)
