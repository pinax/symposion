import operator

from django.contrib.auth.models import User
from django.db.models import Q

from selectable.base import ModelLookup
from selectable.registry import registry


class UserLookup(ModelLookup):
    model = User
    search_fields = (
        'first_name__icontains',
        'last_name__icontains',
        'email__icontains',
    )

    def get_query(self, request, term):
        qs = self.get_queryset()
        if term:
            search_filters = []
            if len(term.split()) == 1:
                if self.search_fields:
                    for field in self.search_fields:
                        search_filters.append(Q(**{field: term}))
                qs = qs.filter(reduce(operator.or_, search_filters))
            else:
                # Accounts for 'John Doe' term; will compare against get_full_name
                term = term.lower()
                qs = [x for x in qs if term in x.get_full_name().lower()]
        return qs

    def get_item_value(self, item):
        return item.email

    def get_item_label(self, item):
        return u"%s (%s)" % (item.get_full_name(), item.email)

    def create_item(self, value):
        """We aren't actually creating a new user, we just need to supply the
           email to the form processor
        """
        return value

registry.register(UserLookup)
