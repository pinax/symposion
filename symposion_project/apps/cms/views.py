from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.models import Page


def page(request, slug):
    
    page = Page.objects.get(path=slug)
    
    return render_to_response("cms/page_detail.html", {
        "page": page,
    }, context_instance=RequestContext(request))
