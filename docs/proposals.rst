Proposals App
=============


Models
------


ProposalSection
~~~~~~~~~~~~~~~

Recall that a symposion instance consists of one or more ``Conference``s each
made up of one or more ``Section``s.

Different sections can have different open / close dates for proposals.
This is managed through a ``ProposalSection`` which is a one-to-one with
``Section`` where you can define a ``start`` date, an ``end`` date and/or
simply toggle proposals for the section ``closed``.

A section is available for proposals iff:
 * it is after the ``start`` (if there is one) and
 * it is before the ``end`` (if there is one) and
 * ``closed`` is NULL or False

In other words, ``closed`` can be used as an override, regardless of ``start``
and ``end`` and, if you want, you can just manually use ``closed`` rather than
setting dates.

This model is currently managed by conference staff via the Django admin
although given it's part of "conference setup", it may often just be a
fixture that's loaded.


ProposalKind
~~~~~~~~~~~~

A conference, even within a section, may have different kinds of
presentations, e.g. talks, panels, tutorials, posters.

If these have different requirements for what fields should be in the
proposal form, they should be modeled as different ``ProposalKind``s. For
example, you may want talk proposals to include an intended audience level
but not require that for poster submissions.

Note that if you have different deadlines, reviews, etc. you'll want to
distinguish the **section** as well as the kind.

This model is currently managed by conference staff via the Django admin
although given it's part of "conference setup", it may often just be a
fixture that's loaded.


ProposalBase
~~~~~~~~~~~~

Each proposal kind should have a subclass of ``ProposalBase`` defining the
fields for proposals of that kind. We discuss below how that association is
made.

``ProposalBase`` provides fields for a ``title``, a single-paragraph
plain-text ``description`` and an ``abstract`` which can contain markup.

There is also an ``additional_notes`` field which can be used for speakers to
communicate additional information about their proposal to reviewers that is
not intended to be shared with others.

This base model supports each proposal having multiple speakers (although
the submitting speaker is always treated differently) and also supports
the attachments of supporting documents for reviewers that are, like the
``additional_notes`` not intended to be shared with others.

A ``cancelled`` boolean field is also provided to indicate that a proposal
has been cancelled or withdrawn.


AdditionalSpeaker
~~~~~~~~~~~~~~~~~

Used for modeling the additional speakers on a proposal in additional to the
submitting speaker. The status of an additional speaker may be ``Pending``,
``Accepted`` or ``Declined``.

.. todo:: see note in speakers docs about explaining the flow


SupportingDocument
~~~~~~~~~~~~~~~~~~

Used for modeling the supporting documents that can be attached to a proposal.


How to Add Custom Proposal Kinds
--------------------------------

For each kind:

 * create a ``ProposalKind`` instance
 * subclass ``ProposalBase`` and add the fields you want
 * define a Django ``ModelForm`` for proposals of that kind
 * make sure your settings file has a ``PROPOSAL_FORMS`` dictionary
   that maps the slug of your ``ProposalKind`` to the fully-qualified
   name of your ``ModelForm``.

For example::
    
    PROPOSAL_FORMS = {
        "tutorial": "pycon.forms.PyConTutorialProposalForm",
        "talk": "pycon.forms.PyConTalkProposalForm",
        "poster": "pycon.forms.PyConPosterProposalForm",
    }

