from constance import config
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from django.http import Http404
from django.shortcuts import render_to_response, redirect, render, \
    get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from symposion.sponsorship.forms import SponsorApplicationForm, \
    SponsorDetailsForm, SponsorBenefitsFormSet, SponsorEmailForm
from symposion.sponsorship.models import Sponsor, SponsorBenefit


@login_required
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save()
            if sponsor.sponsor_benefits.all():
                # Redirect user to sponsor_detail to give extra information.
                messages.success(request, "Thank you for your sponsorship "
                                 "application. Please update your "
                                 "benefit details below.")
                return redirect("sponsor_detail", pk=sponsor.pk)
            else:
                messages.success(request, "Thank you for your sponsorship "
                                 "application.")
                return redirect("dashboard")
    else:
        form = SponsorApplicationForm(user=request.user)

    return render_to_response("sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_add(request):
    if not request.user.is_staff:
        raise Http404()

    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.active = True
            sponsor.save()
            return redirect("sponsor_detail", pk=sponsor.pk)
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


@staff_member_required
def sponsor_email(request, pks):
    sponsors = Sponsor.objects.filter(pk__in=pks.split(","))

    address_list = []
    for sponsor in sponsors:
        if sponsor.contact_email.lower() not in address_list:
            address_list.append(sponsor.contact_email.lower())
        if sponsor.applicant.email.lower() not in address_list:
            address_list.append(sponsor.applicant.email.lower())

    initial = {
        'from_': config.SPONSOR_FROM_EMAIL,
    }

    # Note: on initial entry, we've got the request from the admin page,
    # which was actually a POST, but not from our page. So be careful to
    # check if it's a POST and it looks like our form.
    if request.method == 'POST' and 'subject' in request.POST:
        form = SponsorEmailForm(request.POST, initial=initial)
        if form.is_valid():
            data = form.cleaned_data

            # Send emails one at a time, rendering the subject and
            # body as templates.
            for sponsor in sponsors:
                address_list = []
                if sponsor.contact_email.lower() not in address_list:
                    address_list.append(sponsor.contact_email.lower())
                if sponsor.applicant.email.lower() not in address_list:
                    address_list.append(sponsor.applicant.email.lower())

                subject = sponsor.render_email(data['subject'])
                body = sponsor.render_email(data['body'])

                mail = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=data['from_'],
                    to=address_list,
                    cc=data['cc'].split(","),
                    bcc=data['bcc'].split(",")
                )
                mail.send()
            messages.add_message(request, messages.INFO, _(u"Email sent to sponsors"))
            return redirect(reverse('admin:sponsorship_sponsor_changelist'))
    else:
        form = SponsorEmailForm(initial=initial)
        context = {
            'address_list': address_list,
            'form': form,
            'pks': pks,
            'sponsors': sponsors,
        }
    return render(request, "sponsorship/email.html", context)
