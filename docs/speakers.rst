Speaker App
===========

The ``speaker`` app allows speakers to set up their profile, prior to or as
part of the proposal submission phase. The **dashboard** is the means through
which speakers manage their own profiles.

We are planning to make the Speaker model more pluggable so, if you have
particular fields you'd like your speakers to fill out, you'll be able to
customize things more easily.

Additional Speakers
-------------------

Because ``symposion`` supports additional speakers being attached to a
proposal or actual presentation, it has the notion of a ``Speaker`` that is
not yet a ``User`` on the site. For this reason, a ``Speaker`` may have a
NULL ``user`` field (hopefully temporarily) as well as an ``invite_email``
and ``invite_token`` field for the invitation sent to the additional speaker
to join.

.. todo:: perhaps explain the invitation flow
