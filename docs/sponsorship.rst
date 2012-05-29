Sponsorship App
===============

Sponsorship is managed via the ``sponsorship`` app.

Sponsorship levels and sponsors are added via the Django admin.


Models
------

Each sponsor level has a ``name`` (e.g. "Gold", "Silver") and an ``order``
field which is an integer that is used to sort levels (lowest first). Each
level also has a ``description`` which is not currently exposed anywhere
but can be used for private annotation.

Each sponsor has a ``name``, ``external_url`` (i.e. link to the sponsor's
website), ``contact_name`` and ``contact_email``, ``logo``, and ``level``.

A sponsor may also have a private ``annotation`` that can be used by
organizers to take notes about the sponsor.

A sponsor will not appear on the site until the ``active`` flag is set true.


Template Snippets
-----------------

The easiest way to include sponsor logos, grouped by level, is to either::

    {% include "sponsorship/_vertical_by_level.html" %}

or::
    
    {% include "sponsorship/_horizontal_by_level.html" %}

You can get a wall of sponsors (without level designation) with::

    {% include "sponsorship/_wall.html" %}


You can always tweak these templates or use them as the basis for your own.
This is often all you'll need to do to display sponsors on your site.

If you want to display a specific sponsor logo you can use::

    {% include "sponsorship/_sponsor_link.html" with sponsor=sponsor %}

or::
    
    {% include "sponsorship/_sponsor_link.html" with sponsor=sponsor dimensions="100x100" %}

if you want different dimensions than the default 150 x 150.


Template Tags
-------------

If you want to retrieve the sponsors and traverse them yourself, you can use
the provided template tags::

    {% load sponsorship_tags %}
    
    {% sponsors as all_sponsors %}

or::

    {% load sponsorship_tags %}
    
    {% sponsors "Gold" as gold_sponsors %}

if you want to just get a specific level.


You can get the levels with::

    {% load sponsorship_tags %}
    
    {% sponsor_levels as levels %}

and you can always iterate over those levels, calling ``level.sponsors`` to
get the sponsors at that level.
