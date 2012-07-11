from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from cms.models import Page


def page(request, slug):
    
    page = get_object_or_404(Page, path=slug)
    siblings = page.get_siblings(include_self=True)
    
    return render_to_response("cms/page_detail.html", {
        "page": page,
        "siblings": siblings,
    }, context_instance=RequestContext(request))
