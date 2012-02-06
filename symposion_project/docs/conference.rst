Conference App
==============

The overall conference settings are managed via the ``conference`` app.

Conferences and their sections are added and configured via the Django admin.


Models
------

Each conference needs an instance of a ``Conference`` model. In most cases you
will only need one of these but Symposion does support multiple conferences
sharing a database. Similar to the Django Sites framework, the conference your
project is for is selected by the ``CONFERENCE_ID`` setting which defaults to
``1`` but can be changed to the pk of another conference if you have more than
one.

The conference model has an optional ``start_date`` and ``end_date``
indicating when the conference will run. These are optional so you can begin
to configure your conference even if you don't know the exact dates.

The conference model also has a ``timezone`` field which you should set to the
timezone your conference will be in.

There is also a ``Section`` model. This is useful if your conference has
different parts to it that run of different days with a different management,
review or scheduling process. Example of distinct sections might be
"Tutorials", "Talks", "Workshops", "Sprints", "Expo". Many aspects of
Symposion can be configured on a per-section basis.

Each section has an optional ``start_date`` and ``end_date`` similar to the
overall conference.


Helper Functions
----------------

A ``conference.models.current_conference()`` function exists to retrieve the
``Conference`` selected by ``CONFERENCE_ID``.
