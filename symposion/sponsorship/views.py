from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from symposion.sponsorship.forms import SponsorApplicationForm, SponsorDetailsForm, SponsorBenefitsFormSet
from symposion.sponsorship.models import Sponsor, SponsorBenefit


@login_required
def sponsor_apply(request):
    # We're not using this view; disable it (so it's not runnable but doesn't
    # cause spurious merge conflicts)
    raise Http404()
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save()
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user)
    
    return render_to_response("sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_add(request):
    # We're not using this view; disable it (so it's not runnable but doesn't
    # cause spurious merge conflicts)
    raise Http404()
    if not request.user.is_staff:
        raise Http404()
    
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.active = True
            sponsor.save()
            return redirect("dashboard")
    else:
        form = SponsorApplicationForm(user=request.user)
    
    return render_to_response("sponsorship/add.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    
    if sponsor.applicant != request.user:
        return redirect("sponsor_list")
    
    formset_kwargs = {
        "instance": sponsor,
        "queryset": SponsorBenefit.objects.filter(active=True)
    }
    
    if request.method == "POST":
        
        form = SponsorDetailsForm(request.POST, instance=sponsor)
        formset = SponsorBenefitsFormSet(request.POST, request.FILES, **formset_kwargs)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, "Sponsorship details have been updated")
            
            return redirect("dashboard")
    else:
        form = SponsorDetailsForm(instance=sponsor)
        formset = SponsorBenefitsFormSet(**formset_kwargs)
    
    return render_to_response("sponsorship/detail.html", {
        "sponsor": sponsor,
        "form": form,
        "formset": formset,
    }, context_instance=RequestContext(request))
