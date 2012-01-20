from django.http import HttpResponse
from django.views.decorators.http import require_POST

from biblion import creole_parser


@require_POST
def creole_preview(request):
    if "raw" not in request.POST:
        return HttpResponse("no good")
    return HttpResponse(creole_parser.parse(request.POST["raw"]))