from django import template
from django.core.urlresolvers import reverse

from symposion.boxes.models import Box
from symposion.boxes.forms import BoxForm
from symposion.boxes.authorization import load_can_edit


register = template.Library()


@register.inclusion_tag("boxes/box.html", takes_context=True)
def box(context, label, show_edit=True, *args, **kwargs):

    request = context["request"]
    can_edit = load_can_edit()(request, *args, **kwargs)

    try:
        box = Box.objects.get(label=label)
    except Box.DoesNotExist:
        box = None

    if can_edit and show_edit:
        form = BoxForm(instance=box, prefix=label)
        form_action = reverse("box_edit", args=[label])
    else:
        form = None
        form_action = None

    return {
        "request": request,
        "label": label,
        "box": box,
        "form": form,
        "form_action": form_action,
    }
