from django.conf import settings
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import static

from .models import Page, File
from .forms import PageForm, FileUploadForm


def can_edit(user):
    if user.is_staff or user.is_superuser:
        return True
    if user.has_perm("cms.change_page"):
        return True
    return False


def can_upload(user):
    if user.is_staff or user.is_superuser:
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


def file_index(request):
    if not can_upload(request.user):
        raise Http404
    
    ctx = {
        "files": File.objects.all(),
    }
    return render(request, "cms/file_index.html", ctx)


def file_create(request):
    if not can_upload(request.user):
        raise Http404
    
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.commit_on_success():
                kwargs = {
                    "file": form.cleaned_data["file"],
                }
                File.objects.create(**kwargs)
            return redirect("file_index")
    else:
        form = FileUploadForm()
    
    ctx = {
        "form": form,
    }
    return render(request, "cms/file_create.html", ctx)


def file_download(request, pk, *args):
    file = get_object_or_404(File, pk=pk)
    
    if getattr(settings, "USE_X_ACCEL_REDIRECT", False):
        response = HttpResponse()
        response["X-Accel-Redirect"] = file.file.url
        # delete content-type to allow Gondor to determine the filetype and
        # we definitely don't want Django's default :-)
        del response["content-type"]
    else:
        response = static.serve(request, file.file.name, document_root=settings.MEDIA_ROOT)
    
    return response


def file_delete(request, pk):
    if not can_upload(request.user):
        raise Http404
    
    file = get_object_or_404(File, pk=pk)
    if request.method == "POST":
        file.delete()
        # @@@ message
    return redirect("file_index")
