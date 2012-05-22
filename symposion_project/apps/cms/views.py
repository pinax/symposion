from django.shortcuts import render_to_response
from django.template import RequestContext

from cms.models import Page


def page(request, slug):
    
    page = Page.objects.get(path=slug)
    siblings = page.get_siblings(include_self=True)
    
    return render_to_response("cms/page_detail.html", {
        "page": page,
        "siblings": siblings,
    }, context_instance=RequestContext(request))
