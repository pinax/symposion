from django.http import Http404
from django.shortcuts import render, redirect
from django.template import RequestContext

from .models import Page
from .forms import PageForm


def can_edit(user):
    if user.is_staff or user.is_superuser:
        return True
    if user.has_perm("cms.change_page"):
        return True
    return False


def page(request, path):
    
    editable = can_edit(request.user)
    try:
        page = Page.published.get(path=path)
    except Page.DoesNotExist:
        if editable:
            return redirect("cms_page_edit", path=path)
        else:
            raise Http404
    
    return render(request, "cms/page_detail.html", {
        "page": page,
        "editable": editable,
    })


def page_edit(request, path):
    
    if not can_edit(request.user):
        raise Http404
    
    try:
        page = Page.published.get(path=path)
    except Page.DoesNotExist:
        page = None
    
    if request.method == "POST":
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save(commit=False)
            page.path = path
            page.save()
            return redirect(page)
        else:
            print form.errors
    else:
        form = PageForm(instance=page, initial={"path": path})
    
    return render(request, "cms/page_edit.html", {
        "path": path,
        "form": form
    })
