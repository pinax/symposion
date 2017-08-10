Speaker App
===========

The ``speaker`` app allows speakers to set up their profile, prior to or as
part of the proposal submission phase. The **dashboard** is the means through
which speakers manage their own profiles.


Additional Speakers
-------------------

Because ``symposion`` supports additional speakers being attached to a
proposal or actual presentation, it has the notion of a ``Speaker`` that is
not yet a ``User`` on the site. For this reason, a ``Speaker`` may have a
NULL ``user`` field (hopefully temporarily) as well as an ``invite_email``
and ``invite_token`` field for the invitation sent to the additional speaker
to join.

.. todo:: perhaps explain the invitation flow


Pluggable Speaker Models and Forms
----------------------------------

By default, Symposion uses `DefaultSpeakerModel` and `DefaultSpeakerForm` to
manage speaker profiles. Often you will want to include extra fields in your
speaker model. This was previously not possible without forking Symposion.

If you want to extend the speaker model, you will
need to do the following:

- Create a model that extends `SpeakerBase`
- In your site's `settings.py` file, add a setting for
  `SYMPOSION_SPEAKER_MODEL`. This should be the fully qualified location of
  your new speaker model, e.g. `pinaxcon.customizations.models.CustomSpeaker`

`DefaultSpeakerForm` is a `ModelForm` based on either the model specified as
`SYMPOSION_SPEAKER_MODEL`, or  `DefaultSpeaker` if you don't specify your own
model type. Its default behaviour is to display all of the fields on your
model, except for some fields that are used internally to manage the additional
speaker invitation flow. This should be good enough for most applications.

If you want to customize your form beyond this, you will need to do the
following:

- Create a `ModelForm` that saves your custom speaker model
- In your site's `settings.py` file, add a setting for
  `SYMPOSION_SPEAKER_FORM`



Migrating your customized Symposion speaker models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to migrate customised Symposion speaker models. Running the
migrations that introduce pluggable speaker profiles moves `twitter_username`
over to the new `DefaultSpeaker` model.

Generally you'll need to consider the following when making a migration:

- Ensuring that `ProposalBase` and `AdditionalSpeaker` links are maintained
- Any Model that previously depended upon `Speaker` has its links updated

However, if you are maintaining a customised Symposion speaker model, it is
likely that you have already forked Symposion. In this case, there'll be
diminishing returns to migrating over to the new model for your existing apps.
