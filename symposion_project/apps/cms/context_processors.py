from cms.models import MenuItem


def menuitems(request):
    qs = MenuItem.objects.filter(published=True)
    if not request.user.is_authenticated():
        qs = qs.filter(login_required=False)
    return {
        "menuitems": qs,
    }
