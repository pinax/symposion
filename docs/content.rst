Content Management
==================

The content management system allows organizers to create pages and page
sections for a conference.  You may want to have an entire page about a job
fair, or may only want to have an editable section at the top of a tutorial
schedule with some instructions for all of the tutorial attendees.

CMS App
-------

The ``cms`` app provides functionality for creating wiki pages. These pages can
be created using the django admin. The django admin form has controls for
specifying:

* title
* markup content
* url path
* tags
* public or draft mode
* publication date

Page content and title can also be edited directly at the url. The ``cms`` app
uses the `django-reversion <http://django-reversion.readthedocs.org>`_ package,
thus content is version controlled.

Boxes App
---------

The ``boxes`` app allows for sections of a page to be edited like a wiki. To use this in a template
use the ``boxes_tags`` and specify a box section of a page using the ``boxes`` tag:

.. code-block:: django

    {% load boxes_tags %}
    {% boxes "intro_section" %}

This template will render an editable content box. When a staff user visits the
page,  they will see an ``Edit this content`` button. The ``boxes`` app also uses the
``django-reversion`` package.
