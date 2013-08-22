Sponsorship App
===============

Sponsorship is managed via the ``sponsorship`` app.

Sponsorship levels are added and benefits managed via the Django admin. 

Sponsors may register their sponsorship in the dashboard. If sponsor applies, staff will need to approve the pending sponsorship (click sponsor name in dashboard and check "active" box on next page) before that sponsor will appear on the website. 

Sponsors may also be added by staff, in which case staff can choose to tick "active" box at application submission or may return to make active at a later time. 

Staff users can, at any time, edit sponsor information and assets entered by themselves, other staff, or sponsors by clicking on the appropriate sponsor link in the dashboard under "Sponsorship".


Models
------

SponsorLevel
~~~~~~~~~~~~~~~

Each sponsor level has a ``name`` (e.g. "Gold", "Silver") and an ``order``
field which is an integer that is used to sort levels (lowest first). Each
level also has a ``description`` which is not currently exposed anywhere
but can be used for private annotation.

Sponsor
~~~~~~~~~

Each sponsor has a ``name``, ``external_url`` (i.e. link to the sponsor's
website), ``contact_name`` and ``contact_email``, ``logo``, and ``level``.

A sponsor may also have a private ``annotation`` that can be used by
organizers to take notes about the sponsor.

A sponsor will not appear on the site until the ``active`` flag is set true.
Note:: If using {% sponsors as all_sponsors %}, you'll need to use the "is_active" filter in your implementation to achieve this, ie {% for sponsor in all_sponsors|is_active %}. It is not necessary to use this filter when using template tag {% sponsor_levels as levels %}.

Benefit
~~~~~~~~~

Each benefit has a ``name``, a ``description``, and a ``type``.

BenefitLevel
~~~~~~~~~~~~~~

Each benefit may belong to one or more benefit levels, and is given default limits depending on the level by associating ``benefit`` and ``level``.

SponsorBenefit
~~~~~~~~~~~~~~~~

Stores benefits for each sponsor by associating ``sponsor`` and ``benefit``, and handles data entered in sponsor application (logo, text, etc.)



Template Snippets
--------------------

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

Note:: This tag only needs the "is_active" filter when using, ie {% for sponsor in all_sponsors|is_active %}, where the intention is to show active/approved sponsors and not also sponsors whose status is "pending"

or::

    {% load sponsorship_tags %}
    
    {% sponsors "Gold" as gold_sponsors %}

if you want to just get a specific level.


You can get the levels with::

    {% load sponsorship_tags %}
    
    {% sponsor_levels as levels %}

and you can always iterate over those levels, calling ``level.sponsors`` to
get the sponsors at that level.
